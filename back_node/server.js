const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const PORT = 8080;

// ---------- Configuración de la base de datos ----------
// Usa variables de entorno o valores por defecto (modifícalos según tu entorno)
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'oxdiccionariodb',
  password: process.env.DB_PASSWORD || 'password2017',
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
//createTable();


// ******************* 
// Rutas  diccionario
// ******************* 
 
console.log('GET /diccionario');
// GET /diccionario - Obtener todos
app.get('/diccionario', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM diccionario ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /diccionario/:id');
// GET /diccionario/:id - Obtener uno por ID
app.get('/diccionario/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM diccionario WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /diccionario')
// POST /diccionario - Crear un nuevo usuario
app.post('/diccionario', async (req, res) => {
  const { grupo,texto,lenguajes_id,nivel_id,tipodiccionario_id,tipopalabra_id } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO diccionario (grupo,texto,lenguajes_id,nivel_id,tipodiccionario_id,tipopalabra_id) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *',
      [grupo,texto,lenguajes_id,nivel_id,tipodiccionario_id,tipopalabra_id]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /diccionario/:id')
// PUT /diccionario/:id - Actualizar un usuario existente
app.put('/diccionario/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { grupo,texto,lenguajes_id,nivel_id,tipodiccionario_id,tipopalabra_id } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(grupo){ fields.push(`grupo = $${idx++}`);values.push(grupo);} if(texto){ fields.push(`texto = $${idx++}`);values.push(texto);} if(lenguajes_id){ fields.push(`lenguajes_id = $${idx++}`);values.push(lenguajes_id);} if(nivel_id){ fields.push(`nivel_id = $${idx++}`);values.push(nivel_id);} if(tipodiccionario_id){ fields.push(`tipodiccionario_id = $${idx++}`);values.push(tipodiccionario_id);} if(tipopalabra_id){ fields.push(`tipopalabra_id = $${idx++}`);values.push(tipopalabra_id);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE diccionario SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /diccionario/:id')
// DELETE /diccionario/:id - Eliminar un usuario
app.delete('/diccionario/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM diccionario WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  images
// ******************* 
 
console.log('GET /images');
// GET /images - Obtener todos
app.get('/images', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM images ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /images/:id');
// GET /images/:id - Obtener uno por ID
app.get('/images/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM images WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /images')
// POST /images - Crear un nuevo usuario
app.post('/images', async (req, res) => {
  const { gallery,image } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO images (gallery,image) VALUES ($1,$2) RETURNING *',
      [gallery,image]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /images/:id')
// PUT /images/:id - Actualizar un usuario existente
app.put('/images/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { gallery,image } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(gallery){ fields.push(`gallery = $${idx++}`);values.push(gallery);} if(image){ fields.push(`image = $${idx++}`);values.push(image);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE images SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /images/:id')
// DELETE /images/:id - Eliminar un usuario
app.delete('/images/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM images WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  lenguajes
// ******************* 
 
console.log('GET /lenguajes');
// GET /lenguajes - Obtener todos
app.get('/lenguajes', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM lenguajes ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /lenguajes/:id');
// GET /lenguajes/:id - Obtener uno por ID
app.get('/lenguajes/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM lenguajes WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /lenguajes')
// POST /lenguajes - Crear un nuevo usuario
app.post('/lenguajes', async (req, res) => {
  const { lenguaje,siglas } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO lenguajes (lenguaje,siglas) VALUES ($1,$2) RETURNING *',
      [lenguaje,siglas]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /lenguajes/:id')
// PUT /lenguajes/:id - Actualizar un usuario existente
app.put('/lenguajes/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { lenguaje,siglas } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(lenguaje){ fields.push(`lenguaje = $${idx++}`);values.push(lenguaje);} if(siglas){ fields.push(`siglas = $${idx++}`);values.push(siglas);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE lenguajes SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /lenguajes/:id')
// DELETE /lenguajes/:id - Eliminar un usuario
app.delete('/lenguajes/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM lenguajes WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  nivel
// ******************* 
 
console.log('GET /nivel');
// GET /nivel - Obtener todos
app.get('/nivel', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM nivel ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /nivel/:id');
// GET /nivel/:id - Obtener uno por ID
app.get('/nivel/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM nivel WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /nivel')
// POST /nivel - Crear un nuevo usuario
app.post('/nivel', async (req, res) => {
  const { nivel } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO nivel (nivel) VALUES ($1) RETURNING *',
      [nivel]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /nivel/:id')
// PUT /nivel/:id - Actualizar un usuario existente
app.put('/nivel/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { nivel } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(nivel){ fields.push(`nivel = $${idx++}`);values.push(nivel);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE nivel SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /nivel/:id')
// DELETE /nivel/:id - Eliminar un usuario
app.delete('/nivel/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM nivel WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  oxdiscussioncomments
// ******************* 
 
console.log('GET /oxdiscussioncomments');
// GET /oxdiscussioncomments - Obtener todos
app.get('/oxdiscussioncomments', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM oxdiscussioncomments ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /oxdiscussioncomments/:id');
// GET /oxdiscussioncomments/:id - Obtener uno por ID
app.get('/oxdiscussioncomments/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM oxdiscussioncomments WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /oxdiscussioncomments')
// POST /oxdiscussioncomments - Crear un nuevo usuario
app.post('/oxdiscussioncomments', async (req, res) => {
  const { comment,discussionid,time,username } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO oxdiscussioncomments (comment,discussionid,time,username) VALUES ($1,$2,$3,$4) RETURNING *',
      [comment,discussionid,time,username]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /oxdiscussioncomments/:id')
// PUT /oxdiscussioncomments/:id - Actualizar un usuario existente
app.put('/oxdiscussioncomments/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { comment,discussionid,time,username } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(comment){ fields.push(`comment = $${idx++}`);values.push(comment);} if(discussionid){ fields.push(`discussionid = $${idx++}`);values.push(discussionid);} if(time){ fields.push(`time = $${idx++}`);values.push(time);} if(username){ fields.push(`username = $${idx++}`);values.push(username);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE oxdiscussioncomments SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /oxdiscussioncomments/:id')
// DELETE /oxdiscussioncomments/:id - Eliminar un usuario
app.delete('/oxdiscussioncomments/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM oxdiscussioncomments WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  roles
// ******************* 
 
console.log('GET /roles');
// GET /roles - Obtener todos
app.get('/roles', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM roles ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /roles/:id');
// GET /roles/:id - Obtener uno por ID
app.get('/roles/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM roles WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /roles')
// POST /roles - Crear un nuevo usuario
app.post('/roles', async (req, res) => {
  const { roles,siglas } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO roles (roles,siglas) VALUES ($1,$2) RETURNING *',
      [roles,siglas]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /roles/:id')
// PUT /roles/:id - Actualizar un usuario existente
app.put('/roles/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { roles,siglas } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(roles){ fields.push(`roles = $${idx++}`);values.push(roles);} if(siglas){ fields.push(`siglas = $${idx++}`);values.push(siglas);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE roles SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /roles/:id')
// DELETE /roles/:id - Eliminar un usuario
app.delete('/roles/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM roles WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  tipodediccionario
// ******************* 
 
console.log('GET /tipodediccionario');
// GET /tipodediccionario - Obtener todos
app.get('/tipodediccionario', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM tipodediccionario ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /tipodediccionario/:id');
// GET /tipodediccionario/:id - Obtener uno por ID
app.get('/tipodediccionario/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM tipodediccionario WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /tipodediccionario')
// POST /tipodediccionario - Crear un nuevo usuario
app.post('/tipodediccionario', async (req, res) => {
  const { tipodiccionario } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO tipodediccionario (tipodiccionario) VALUES ($1) RETURNING *',
      [tipodiccionario]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /tipodediccionario/:id')
// PUT /tipodediccionario/:id - Actualizar un usuario existente
app.put('/tipodediccionario/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { tipodiccionario } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(tipodiccionario){ fields.push(`tipodiccionario = $${idx++}`);values.push(tipodiccionario);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE tipodediccionario SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /tipodediccionario/:id')
// DELETE /tipodediccionario/:id - Eliminar un usuario
app.delete('/tipodediccionario/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM tipodediccionario WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  tipodepalabra
// ******************* 
 
console.log('GET /tipodepalabra');
// GET /tipodepalabra - Obtener todos
app.get('/tipodepalabra', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM tipodepalabra ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /tipodepalabra/:id');
// GET /tipodepalabra/:id - Obtener uno por ID
app.get('/tipodepalabra/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM tipodepalabra WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /tipodepalabra')
// POST /tipodepalabra - Crear un nuevo usuario
app.post('/tipodepalabra', async (req, res) => {
  const { palabra } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO tipodepalabra (palabra) VALUES ($1) RETURNING *',
      [palabra]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /tipodepalabra/:id')
// PUT /tipodepalabra/:id - Actualizar un usuario existente
app.put('/tipodepalabra/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { palabra } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(palabra){ fields.push(`palabra = $${idx++}`);values.push(palabra);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE tipodepalabra SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /tipodepalabra/:id')
// DELETE /tipodepalabra/:id - Eliminar un usuario
app.delete('/tipodepalabra/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM tipodepalabra WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  users
// ******************* 
 
console.log('GET /users');
// GET /users - Obtener todos
app.get('/users', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM users ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /users/:id');
// GET /users/:id - Obtener uno por ID
app.get('/users/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /users')
// POST /users - Crear un nuevo usuario
app.post('/users', async (req, res) => {
  const { apellido,avatar,edad,email,emailverified,fechadenacimiento,incambioclave,nombre,password,remembertoken,userrole_id,usuario,lenguajesnativo_id } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO users (apellido,avatar,edad,email,emailverified,fechadenacimiento,incambioclave,nombre,password,remembertoken,userrole_id,usuario,lenguajesnativo_id) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING *',
      [apellido,avatar,edad,email,emailverified,fechadenacimiento,incambioclave,nombre,password,remembertoken,userrole_id,usuario,lenguajesnativo_id]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /users/:id')
// PUT /users/:id - Actualizar un usuario existente
app.put('/users/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { apellido,avatar,edad,email,emailverified,fechadenacimiento,incambioclave,nombre,password,remembertoken,userrole_id,usuario,lenguajesnativo_id } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(apellido){ fields.push(`apellido = $${idx++}`);values.push(apellido);} if(avatar){ fields.push(`avatar = $${idx++}`);values.push(avatar);} if(edad){ fields.push(`edad = $${idx++}`);values.push(edad);} if(email){ fields.push(`email = $${idx++}`);values.push(email);} if(emailverified){ fields.push(`emailverified = $${idx++}`);values.push(emailverified);} if(fechadenacimiento){ fields.push(`fechadenacimiento = $${idx++}`);values.push(fechadenacimiento);} if(incambioclave){ fields.push(`incambioclave = $${idx++}`);values.push(incambioclave);} if(nombre){ fields.push(`nombre = $${idx++}`);values.push(nombre);} if(password){ fields.push(`password = $${idx++}`);values.push(password);} if(remembertoken){ fields.push(`remembertoken = $${idx++}`);values.push(remembertoken);} if(userrole_id){ fields.push(`userrole_id = $${idx++}`);values.push(userrole_id);} if(usuario){ fields.push(`usuario = $${idx++}`);values.push(usuario);} if(lenguajesnativo_id){ fields.push(`lenguajesnativo_id = $${idx++}`);values.push(lenguajesnativo_id);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE users SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /users/:id')
// DELETE /users/:id - Eliminar un usuario
app.delete('/users/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM users WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 
// ******************* 
// Rutas  usersroles
// ******************* 
 
console.log('GET /usersroles');
// GET /usersroles - Obtener todos
app.get('/usersroles', async (req, res) => {
try {
    const result = await pool.query('SELECT * FROM usersroles ORDER BY id');
       if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No Existen Registros' });
       } else {
           return res.json(result.rows);
       }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});
 
console.log('GET /usersroles/:id');
// GET /usersroles/:id - Obtener uno por ID
app.get('/usersroles/:id', async (req, res) => {
const id = parseInt(req.params.id);
if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('SELECT * FROM usersroles WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });
  }
});
 
console.log('POST /usersroles')
// POST /usersroles - Crear un nuevo usuario
app.post('/usersroles', async (req, res) => {
  const { role_id,user_id } = req.body;
  //if (!nombre || !correo) {
  //  return res.status(400).json({ error: 'Los campos  son requeridos' });
  //}
  try {
    const result = await pool.query(
      'INSERT INTO usersroles (role_id,user_id) VALUES ($1,$2) RETURNING *',
      [role_id,user_id]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }
});
 
console.log('PUT /usersroles/:id')
// PUT /usersroles/:id - Actualizar un usuario existente
app.put('/usersroles/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  const { role_id,user_id } = req.body;
  //if (!nombre && !correo) {
  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });
  //}
 
  // Construir dinámicamente la consulta de actualización
  const fields = [];
  const values = [];
  let idx = 1;
  if(role_id){ fields.push(`role_id = $${idx++}`);values.push(role_id);} if(user_id){ fields.push(`user_id = $${idx++}`);values.push(user_id);} 
  values.push(id); // para la cláusula WHERE
 
  const query = `UPDATE usersroles SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;
 
  try { 
    const result = await pool.query(query, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });
    }
    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });
  }
});
 
console.log('DET /usersroles/:id')
// DELETE /usersroles/:id - Eliminar un usuario
app.delete('/usersroles/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }
  try {
    const result = await pool.query('DELETE FROM usersroles WHERE id = $1 RETURNING *', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    res.status(204).send(); // Sin contenido
  } catch (err) {
    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });
  }
});
 
// ******************* 
 
 

 




// ******************* 
// Rutas  Login de Usuario
// ******************* 

// Login de Usuario
console.log('POST /login')
// POST /verbos_compuestos - Crear un nuevo usuario
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Los campos  son requeridos' });
  }
  try {
    const result = await pool.query('SELECT * FROM users WHERE email = $1 and password = $2', [email,password]);
    if( result.rowCount == 0 ) {
      return res.status(200).json({ error: 'Credenciales Inválidas' });
    } else {
//      return res.json(result.rows[0]);
      return res.status(200).json({ error:'ok' });
      //console.log(res.json(result.rows[0]));
    }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});


// Login de Usuario
console.log('GET /login')
// POST /verbos_compuestos - Crear un nuevo usuario
app.get('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Los campos  son requeridos' });
  }
  try {
    const result = await pool.query('SELECT * FROM users WHERE email = $1 and password = $2', [email,password]);
    if( result.rowCount == 0 ) {
      return res.status(200).json({ error: 'Credenciales Inválidas' });
    } else {
//      return res.json(result.rows[0]);
      return res.status(200).json({ error:'ok' });
      //console.log(res.json(result.rows[0]));
    }
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });
  }
});


// Registrar de Usuario
console.log('POST /registrar')
// POST /verbos_compuestos - Crear un nuevo usuario
app.post('/registrar', async (req, res) => {
  const { nombre, apellido, email, password, usuario } = req.body;
  if (!nombre || !apellido  || !email || !password || !usuario ) {
    return res.status(400).json({ error: 'Los campos  son requeridos' });
  }
  try {
    const result = await pool.query(
      'INSERT INTO users (nombre, apellido, email, password, usuario, inactivo, incambioclave) VALUES ($1, $2, $3, $4, $5, 1, 0) RETURNING *',
      [nombre, apellido, email, password, usuario]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    // Capturar posible violación de unicidad de email
    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL
      return res.status(409).json({ error: 'El Usuario se encuentra Duplicado' });
    }
    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });
  }

});


// Cambiar Contraseña
console.log('POST /contrasenia')
// POST /verbos_compuestos - Crear un nuevo usuario
app.post('/contrasenia', async (req, res) => {
  const { email, usuario, password } = req.body;
  try {

    const result = await pool.query(
      'UPDATE users SET password = $1 WHERE email = $2 RETURNING *',
      [ password, email ]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Registro no encontrado' });
    }
    return res.status(200).json({ error:'ok' });
    //res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Error al actualizar la contrasenia', detalle: err.message });
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


