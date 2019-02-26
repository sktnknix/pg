import psycopg2

def create_db():
    with psycopg2.connect("dbname=study user=%s password=%s" % (login, password)) as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            create table if not exists student (
            id serial primary key,
            name character varying(100) not null,
            gpa numeric(10,2),
            birth timestamp with time zone
            );
            create table if not exists course (
            id serial primary key,
            name character varying(100) not null
            );
            create table if not exists student_on_course(
            id serial primary key,
            student_id integer references student(id) on delete cascade,
            course_id integer references course(id) on delete cascade
            );
            """)
def get_students(course_id):
    with psycopg2.connect("dbname=study user=%s password=%s" % (login, password)) as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            select s.name, c.name from student_on_course s_c 
            join student s on s.id=s_c.student_id 
            join course c on c.id=s_c.course_id where c.id=%s
            """ % course_id)
            result = db_cursor.fetchall()
            return result

def add_students(course_id, students):
    with psycopg2.connect("dbname=study user=%s password=%s" % (login, password)) as db_connection:
        with db_connection.cursor() as db_cursor:
            for student in students:
                db_cursor.execute("""
                do $$
                declare ret_id integer;
                declare course_id_value integer;
                begin
                insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id into ret_id;
                select %s into course_id_value;
                if course_id_value in (select id from course) then insert into student_on_course 
                (student_id, course_id) values (ret_id, course_id_value);
                end if;
                end $$
                """, (student['name'], student['gpa'], student['birth'], course_id))

def add_student(student):
    with psycopg2.connect("dbname=study user=%s password=%s" % (login, password)) as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            insert into student (name, gpa, birth) values (%s, %s, %s);
            select lastval();
            """, (student['name'], student['gpa'], student['birth']))
            last_student_id = db_cursor.fetchone()[0]
            return last_student_id

def get_student(student_id):
    with psycopg2.connect("dbname=study user=%s password=%s" % (login, password)) as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            select name,gpa,birth from student where id=%s
            """ % student_id)
            result = db_cursor.fetchall()
            return result


login = 'test'
password = ''

students = [{
    'name': 'Fil',
    'gpa': 9.5,
    'birth': '11-11-1995'
},
    {
    'name': 'Alexx',
    'gpa': 9.1,
    'birth': '12-03-1987'
},
    {
    'name': 'Bill',
    'gpa': 9.2,
    'birth': '01-11-1989'
}]

student = {
    'name': 'Vasya',
    'gpa': 8.0,
    'birth': '01-01-1900'
}

#create_db()
#get_student(5)
add_student(student)
#add_students(2, students)
#get_students(2)
