import random
from sys import stderr

from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


COMMENDATIONS = [
	'Молодец!',
	'Отлично!',
	'Хорошо!',
	'Гораздо лучше, чем я ожидал!',
	'Ты меня приятно удивил!',
	'Великолепно!',
	'Прекрасно!',
	'Ты меня очень обрадовал!',
	'Именно этого я давно ждал от тебя!',
	'Сказано здорово – просто и ясно!',
	'Ты, как всегда, точен!',
	'Очень хороший ответ!',
	'Талантливо!',
	'Ты сегодня прыгнул выше головы!',
	'Я поражен!',
	'Уже существенно лучше!',
	'Потрясающе!',
	'Замечательно!',
	'Прекрасное начало!',
	'Так держать!',
	'Ты на верном пути!',
	'Здорово!',
	'Это как раз то, что нужно!',
	'Я тобой горжусь!',
	'С каждым разом у тебя получается всё лучше!',
	'Мы с тобой не зря поработали!',
	'Я вижу, как ты стараешься!',
	'Ты растешь над собой!',
	'Ты многое сделал, я это вижу!',
	'Теперь у тебя точно все получится!',
]


def get_schoolkid(name):
	try:
		schoolkid = Schoolkid.objects.get(full_name__contains=name.title())
	except Schoolkid.DoesNotExist:
		stderr.write('Ученика с таким именем не существует.\n' \
					 'Попробуйте еще раз с другим ФИО.\n')
	except Schoolkid.MultipleObjectsReturned:
		stderr.write('Учеников с таким именем несколько.\n' \
					 'Попробуйте еще раз с более полным ФИО.\n')
	else:
		return schoolkid


def fix_marks(schoolkid):
	Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)


def remove_chastisements(schoolkid):
	Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title):
	lesson = Lesson.objects.filter(
		year_of_study=schoolkid.year_of_study,
		group_letter=schoolkid.group_letter,
		subject__title=subject_title.capitalize()
	).order_by('-date').first()

	if lesson is None:
		stderr.write('Предмета с таким названием не существует.\n' \
					 'Попробуйте еще раз с другим предметом.\n')
	else:
		Commendation.objects.create(
			text=random.choice(COMMENDATIONS),
			created=lesson.date,
			schoolkid=schoolkid,
			subject=lesson.subject,
			teacher=lesson.teacher
		)
