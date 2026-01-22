drop database cenit_salud_db;

create database cenit_salud_db;

create table if not exists medicos(
    id_medico int auto_increment,
    nombre varchar(50),
    especialidad varchar(50),
    correo_interno varchar(50),
    primary key(id_medico)
);

create table if not exists pacientes(
    id_paciente int auto_increment,
    nombre varchar(50),
    apellido varchar(50),
    telefono varchar(15),
    email varchar(100),
    primary key(id_paciente)
);

create table if not exists citas(
    id_cita int auto_increment,
    id_paciente int,
    id_medico int,
    fecha_cita date,
    motivo varchar(255),
    primary key(id_cita)
);

ALTER TABLE citas
ADD CONSTRAINT FK_1
FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente);

ALTER TABLE citas
ADD CONSTRAINT FK_2
FOREIGN KEY (id_medico) REFERENCES medicos(id_medico);
