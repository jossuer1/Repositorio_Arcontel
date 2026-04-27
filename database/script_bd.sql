-- =====================================
-- TABLA ROLES
-- =====================================
CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================
-- TABLA PERMISOS
-- =====================================
CREATE TABLE permisos (
    id_permiso SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================
-- TABLA USUARIOS
-- =====================================
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    cedula VARCHAR(10) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    id_rol INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- =====================================
-- TABLA ROLES - PERMISOS
-- =====================================
CREATE TABLE roles_permisos (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,

    PRIMARY KEY (id_rol, id_permiso),

    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso) ON DELETE CASCADE
);

-- =====================================
-- TABLA PERMISOS TEMPORALES
-- =====================================
CREATE TABLE usuarios_permisos_temporales (
    id_permiso_temp SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_permiso INT NOT NULL,

    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP,

    motivo TEXT NOT NULL,
    otorgado_por INT NOT NULL,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso),
    FOREIGN KEY (otorgado_por) REFERENCES usuarios(id_usuario),

    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio)
);

-- =====================================
-- TABLA LOGUEO
-- =====================================
CREATE TABLE logueo (
    id_logueo SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,

    ip_dispositivo INET,
    user_agent TEXT,
    dispositivo VARCHAR(100),

    fecha_logueo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- =====================================
-- TABLA AUDITORIA
-- =====================================
CREATE TABLE auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    id_registro INT,
    accion VARCHAR(20) NOT NULL,
    id_usuario INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalle TEXT,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),

    CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE'))
);

-- =====================================
-- TABLA TAREAS / REPORTES
-- =====================================
CREATE TABLE tareas_reportes (
    id_tarea SERIAL PRIMARY KEY,

    id_usuario_asignado INT,
    id_usuario_creador INT NOT NULL,

    descripcion TEXT,

    estado VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega TIMESTAMP,
    fecha_procesado TIMESTAMP,

    FOREIGN KEY (id_usuario_asignado) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_usuario_creador) REFERENCES usuarios(id_usuario),

    CHECK (estado IN ('PENDIENTE', 'PROCESADO'))
);

-- =====================================
-- TABLA CARGAS
-- =====================================
CREATE TABLE cargas (
    id_carga SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,

    nombre_archivo VARCHAR(255),

    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    filas_registradas INT NOT NULL,

    estado VARCHAR(20) DEFAULT 'PROCESADO',

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),

    CHECK (estado IN ('PENDIENTE', 'PROCESADO', 'ERROR'))
);