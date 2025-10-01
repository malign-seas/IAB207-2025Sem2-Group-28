from website import create_app
# test 2 ibrahim
# meileen test commit on testing branch
if __name__ == '__main__':
    app = create_app()
    app.run()

# create database terminal commands
# python
# >>> from website import db, create_app
# >>> app = create_app()
# >>> ctx = app.app_context()
# >>> ctx.push()
# >>> db.create_all()
