from datetime import datetime, date

from flask import session, redirect, render_template, url_for, request, flash
from src.models import Task, HistoryActions, ActionsType, User, Executions
from src.extentions import db
from . import bp

#CREATE
@bp.route('/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        name = request.form.get('name')
        description = request.form.get('description')
        endtime = request.form.get('endTime')
        startTime = request.form.get('startTime')
        weakday = request.form.get('weakday')

        # Verifica se os campos obrigatórios estão preenchidos
        if not name or not endtime or not startTime or not weakday:
            flash('Precisa preencher todos os campos obrigatórios.', 'error')
            return redirect(url_for('task.create_task'))

        user_id = session['user_id']
        endtime_date = None
        if endtime:
            # Converte a string de data para um objeto DateTime do Python
            endtime_date = datetime.strptime(endtime, '%H:%M').time()
        startTime_date = None
        if startTime:
            # Converte a string de data para um objeto DateTime do Python
            startTime_date = datetime.strptime(startTime, '%H:%M').time()

        
        new_task = Task(
            name=name, 
            description=description, 
            endTime=endtime_date,
            startTime=startTime_date,
            weakday=weakday,
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.flush()  # Garante que o ID da tarefa seja gerado antes de criar o histórico

        # Cria um registro de histórico para a criação da tarefa
        history_entry = HistoryActions(
            actionsType=ActionsType.CREATE,
            description=f'Task "{name}" created for user {user.name}.',
            user_id=user_id,
            rotina_id=new_task.id
        )
        db.session.add(history_entry)
        db.session.commit()
        return redirect(url_for('user.dashboard'))
    return render_template('task/register.html')

#UPDATE
@bp.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        # Novos dados da tarefa
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        new_endTime = request.form.get('endTime')
        new_startTime = request.form.get('startTime')
        new_weakday = request.form.get('weakday')

        # Verifica se os campos obrigatórios estão preenchidos
        if not new_name or not new_endTime or not new_startTime or not new_weakday:
            flash('Precisa preencher todos os campos obrigatórios.', 'error')
            return redirect(url_for('task.update_task', task_id=task_id))

        endTime_date = None
        if new_endTime:
            endTime_date = datetime.strptime(new_endTime, '%H:%M').time()
        startTime_date = None
        if new_startTime:
            startTime_date = datetime.strptime(new_startTime, '%H:%M').time()

        # Atualiza os campos da tarefa
        task.name = new_name
        task.description = new_description
        task.endTime = endTime_date
        task.startTime = startTime_date
        task.weakday = new_weakday
        db.session.add(task)
        db.session.commit()

        # Cria um registro de histórico para a atualização da tarefa
        history_entry = HistoryActions(
            actionsType=ActionsType.UPDATE,
            description=f'Task "{new_name}" updated for user {user.name}.',
            user_id=session['user_id'],
            rotina_id=task.id
        )

        db.session.add(history_entry)
        db.session.commit()
        return redirect(url_for('user.dashboard'))
    return render_template('task/edit.html', task=task)

#DELETE
@bp.route('/delete/<int:task_id>', methods=['POST', 'GET'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user = User.query.get(session['user_id'])
    task = Task.query.get_or_404(task_id)
    task.is_active = False  # Marcar a tarefa como inativa em vez de deletar
    db.session.add(task)
    # Cria um registro de histórico para a exclusão da tarefa
    history_entry = HistoryActions(
        actionsType=ActionsType.DELETE,
        description=f'Task "{task.name}" deleted for user {user.name}.',
        user_id=session['user_id'],
        rotina_id=task.id
    )
    db.session.add(history_entry)
    db.session.commit()
    return redirect(url_for('user.dashboard'))

#CONCLUIR
@bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('user.dashboard'))
    
    task = Task.query.get_or_404(task_id)
    user_id = task.user_id
    user = User.query.get(user_id)

    if not task.is_active:
        flash('Não é possível concluir uma tarefa inativa.', 'error')
        return redirect(url_for('user.dashboard'))
    
    today = date.today()
    execution_conflict = Executions.query.filter_by(rotina_id=task_id, date=today).first()
    if execution_conflict:
        flash('Esta tarefa já foi concluída hoje.', 'error')
        return redirect(url_for('user.dashboard'))
    
    try:
        new_execution = Executions(rotina_id=task_id, date=today)
        db.session.add(new_execution)
        action = HistoryActions(
            actionsType=ActionsType.UPDATE,
            description=f'Task "{task.name}" marked as completed for user {user.name}.',
            user_id=user.id,
            rotina_id=task.id
        )
        db.session.add(action)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Ocorreu um erro ao concluir a tarefa. Tente novamente.', 'error')
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('user.dashboard'))