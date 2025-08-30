CREATE TABLE me_gusta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    inmueble_id INT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_me_gusta_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_me_gusta_inmueble
        FOREIGN KEY (inmueble_id)
        REFERENCES inmuebles(id)
        ON DELETE CASCADE,
    CONSTRAINT uq_me_gusta UNIQUE (usuario_id, inmueble_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
