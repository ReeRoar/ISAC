import requests
import json

IP = '127.0.0.1'
PORT = '5000'
base_url = f'http://{IP}:{PORT}'
session = requests.Session()


def post_data(file_name, object_name, url):
    '''
    Posts the data from a json file
    :param file_name: name of file (without json_files/)
    :param object_name: Name of object named in json list
    :param url: url (after port/) to post the data to
    :return: None
    '''
    f = open(f'json_files/{file_name}')
    data = json.load(f)
    for i in data[object_name]:
        try:
            r = session.post(f'{base_url}/{url}', json=i)
            r.raise_for_status()
        except Exception as e:
            print(f'Error has occurred with load file {file_name}:\n{e}')


session.post(f'{base_url}/users', json={'email': 'jungsemail@hartford.edu',
                                        'password': 'a'})
r = session.post(f'{base_url}/login', json={'email': 'jungsemail@hartford.edu',
                                            'password': 'a'})

r = session.post(f'{base_url}/attendance_count', json={'camera_value': 0,
                                                       'rfid_value': 0,
                                                       'mismatch_counter': 0})

post_data('professor.json', 'professors', 'professors')

post_data('users.json', 'users', 'users')

post_data('course.json', 'courses', 'courses')
post_data('student.json', 'students', 'students')
post_data('attendance.json', 'attendances', 'attendance')

post_data('sign_in.json', 'sign_ins', 'sign_ins')
post_data('professor_assignment.json', 'professor_assignments', 'prof_assignment')
post_data('student_enrollment.json', 'student_enrollments', 'student_enroll')
