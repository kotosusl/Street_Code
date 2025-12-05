# Street_Code
"Код Улиц" - приложение для проведения командных квестов по улицам города

### API: установите все зависимости из requirements.txt и запустите main.py. Сервер запускается на http://127.0.0.1:8080/
## POST /api/auth/register
Регистрация пользователя
input: {email, password, confirm_password, name}
output: {success: bool, message: str, data: {user: {email: str, id: str, role: str, username: str}, tokens: {access_token: str, refresh_token: str, expires_in: int}}}

## POST /api/auth/login
Вход пользователя
input: {email, password}
output: {success: bool, message: str, data: {user: {email: str, id: str, role: str, username: str}, tokens: {access_token: str, refresh_token: str, expires_in: int}}}

## POST /api/auth/refresh
Рефреш токена
input: {refresh_token}
output: {success: bool, message: str, data: {user: {}, tokens: {access_token: str, expires_in: int}}}

## POST /api/auth/logout
Выход пользователя
input: header["Authorization"] = "Bearer {token}"
output: {success: bool, message: str}

## POST /api/check_answer
Проверка отправленного ответа
input: {answer, game_session_id, question_id}
1. Если игра заклнчилась
  output: {status: str, game_status: "finished", start_datetime: DateTime, end_datetime: DateTime, total_score: int, hints: int, registration_id: str}
2. Если игра продолжается
   output: {status: str, game_status: "active", start_datetime: DateTime, total_score: int, hints: int, registration_id: str, correct: bool, question_score: int}

## POST /api/get_one_game
Получение информации об одном квесте
input: {game_id}
output: {game_id: str, title: str, dascription: str, organizer: str, avatar: BLOB, location: str, difficulty: str, duration: int, max_members: int, genre: str, is_active: bool, start_datetime: DateTime, end_datetime: DateTime}

## GET /api/get_quests
Получение списка квестов по фильтру
input: {title, location, difficulty, duration, mode, genre}
output: {searching_quests: [{game_id: str, title: str, dascription: str, organizer: str, avatar: BLOB, location: str, difficulty: str, duration: int, max_members: int, genre: str, is_active: bool, start_datetime: DateTime, end_datetime: DateTime}, ...]}

## POST /api/post_registration
Регистрация команды на игру
input: {game_name: str, team_name: str}
output: {status: str}

## POST /api/start_game
Начало игровой сессии
input: {registration_id}
output: {status: str, game_session: {id: str, start_datetime: DateTime, score: int, hints: int, status: str, registration_id: str, questions_id_list: [{game_id: str, title: str, dascription: str, organizer: str, avatar: BLOB, location: str, difficulty: str, duration: int, max_members: int, genre: str, is_active: bool, start_datetime: DateTime, end_datetime: DateTime}, ...]}}

## Формат ответа ошибок
output: {sucsess: bool, message: str}

