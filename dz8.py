import psycopg2

def create_db():
    with psycopg2.connect("dbname=study user=test") as db_connection:
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
    with psycopg2.connect("dbname=study user=test") as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            select s.name, c.name from student_on_course s_c 
            join student s on s.id=s_c.student_id 
            join course c on c.id=s_c.course_id where c.id=%s
            """ % course_id)
            result = db_cursor.fetchall()
            print(result)

def add_students(course_id, students):
    with psycopg2.connect("dbname=study user=test") as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            do $$
            declare ret_id integer;
            begin
            insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id into ret_id;
            insert into student_on_course (student_id, course_id) values (ret_id, %s);
            end $$
            """, (students['name'], students['gpa'], students['birth'], course_id))

def add_student(student):
    with psycopg2.connect("dbname=study user=test") as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            insert into student (name, gpa, birth) values (%s, %s, %s)
            """, (students['name'], students['gpa'], students['birth']))

def get_student(student_id):
    with psycopg2.connect("dbname=study user=test") as db_connection:
        with db_connection.cursor() as db_cursor:
            db_cursor.execute("""
            select name,gpa,birth from student where id=%s
            """ % student_id)
            result = db_cursor.fetchall()
            print(result)


#create_db()
students = {
    'name': 'Andrey',
    'gpa': 9.5,
    'birth': '11-11-1995'
}

get_student(5)
#add_student(students)
#add_students(3, students)
#get_students(2)
