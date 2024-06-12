import os
current_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)
relative_path_user_data = 'users_data/'
path_user_data = os.path.join(current_directory, relative_path_user_data)
