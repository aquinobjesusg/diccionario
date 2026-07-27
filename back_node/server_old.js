const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const PORT = 8080;

// ---------- Configuración de la base de datos ----------
// Usa variables de entorno o valores por defecto (modifícalos según tu entorno)
const pool = new Pool({
  user: process.env.DB_USER || 'sdp',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'sdp',
  password: process.env.DB_PASSWORD || 'sdp',
  port: process.env.DB_PORT || 5432,
});

// Middleware
app.use(cors());
app.use(express.json());

// ---------- Función para crear la tabla si no existe ----------
const createTable = async () => {
  const query = `
    CREATE TABLE IF NOT EXISTS usuarios (
      id SERIAL PRIMARY KEY,
      nombre VARCHAR(100) NOT NULL,
      correo VARCHAR(100) UNIQUE NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  try {
    await pool.query(query);
    console.log('✅ Tabla "usuarios" asegurada.');
  } catch (err) {
    console.error('❌ Error al crear la tabla:', err.message);
    process.exit(1);
  }
};

// Inicializar la tabla al arrancar
createTable();

// ---------- CRUD para usuarios ----------

console.log('/usuarios');
// GET /usuarios - Obtener todos
app.get('/usuarios', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuarios ORDER BY id');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener usuarios', detalle: err.message });
  }
});

console.log('/usuarios/:id');
// GET /usuarios/:id - Obtener uno por ID
app.get('/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM usuarios WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener usuario', detalle: err.message });
  }
});

// POST /usuarios - Crear un nuevo usuario
app.post('/usuarios', async (req, res) => {
  const { nombre, correo } = req.body;
  if (!nombre || !correo) {
    return res.status(400).json({ error: 'Los campos "nombre" y "correo" son requeridos' });
  }
  try {
    const result = await pool.query(
      'INSERT INTO usuarios (nombre, correo) VALUES ($1, $2) RETURNING *',
      [nombre, email]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El email ya está registrado' });
    }
    res.status(500).json({ error: 'Error al crear usuario', detalle: err.message });
  }
});

// PUT /usuarios/:id - Actualizar un usuario existente
app.put('/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { nombre, correo } = req.body;
  if (!nombre && !correo) {
    return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  }

  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if (nombre) {
    fields.push(`nombre = $${idx++}`);
    values.push(nombre);
  }
  if (correo) {
    fields.push(`correo = $${idx++}`);
    values.push(correo);
  }
  values.push(id); // para la cláusula WHERE

  const query = `UPDATE usuarios SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;

  try {
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'El correo ya está registrado por otro usuario' });
    }
    res.status(500).json({ error: 'Error al actualizar usuario', detalle: err.message });
  }
});

// DELETE /usuarios/:id - Eliminar un usuario
app.delete('/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM usuarios WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar usuario', detalle: err.message });
  }
});

// Ruta 404 para endpoints no definidos
app.use((req, res) => {
  res.status(404).json({ error: 'Ruta no encontrada' });
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});