from celery import Celery

app = Celery('myapp')

@app.task
def my_task(arg1, arg2):
    print("Oi")
    print(arg1 + arg2)
    return arg1 + arg2

if __name__ == '__main__':
    # Chame a tarefa assíncrona usando apply_async em vez de delay para facilitar a execução em scripts
    result = my_task.apply_async(args=(1, 2))
    print("Tarefa agendada. ID da tarefa:", result.id)
