package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"strings"
	"text/tabwriter"

	_ "github.com/lib/pq" // Driver PostgreSQL
)

// Configuración de la conexión (se puede cambiar por variables de entorno)
const (
	host     = "localhost"
	port     = 5432
	user     = "postgres"
	password = "password2017"
	dbname   = "oxdiccionariodb"
)

func main() {
	// Cadena de conexión
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	// Abrir conexión
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		log.Fatal("Error al conectar: ", err)
	}
	defer db.Close()

	// Verificar conexión
	err = db.Ping()
	if err != nil {
		log.Fatal("No se pudo hacer ping a la base de datos: ", err)
	}

	fmt.Println("Conectado a la base de datos exitosamente")

	// Consulta para obtener las tablas (excluyendo las del sistema)
	rowsTables, err := db.Query(`
		SELECT table_name
		FROM information_schema.tables
		WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
		  AND table_type = 'BASE TABLE'
		ORDER BY table_name
	`)
	if err != nil {
		log.Fatal("Error al obtener tablas: ", err)
	}
	defer rowsTables.Close()

	// Crear archivo de salida
	file, err := os.Create("tablas.txt")
	if err != nil {
		log.Fatal("Error al crear archivo: ", err)
	}
	defer file.Close()

	// Usamos tabwriter para formatear en columnas (opcional, pero mejora la legibilidad)
	w := tabwriter.NewWriter(file, 0, 0, 2, ' ', 0)

	// Escribir encabezado
	//fmt.Fprintln(w, "TABLA\tCAMPO\tTIPO\t¿NULO?\tCLAVE PRIMARIA")

	var sbTables strings.Builder

	// Recorrer cada tabla
	for rowsTables.Next() {
		var tableName string
		if err := rowsTables.Scan(&tableName); err != nil {
			log.Fatal("Error al escanear tabla: ", err)
		}

		// Consultar columnas de la tabla
		rowsCols, err := db.Query(`
			SELECT
				column_name,
				data_type,
				is_nullable,
				COALESCE(
					(SELECT 'YES'
					 FROM information_schema.key_column_usage
					 WHERE table_name = $1
					   AND column_name = c.column_name
					   AND constraint_name LIKE '%pkey%'
					), 'NO') AS is_primary
			FROM information_schema.columns c
			WHERE table_name = $1
			ORDER BY ordinal_position
		`, tableName)
		if err != nil {
			log.Printf("Error al obtener columnas de %s: %v", tableName, err)
			continue
		}
		defer rowsCols.Close()

		var sbColumns strings.Builder
		var sbColnums strings.Builder
		var sbUpdateColnums strings.Builder

		intColums := 0
		// Escribir cada columna
		for rowsCols.Next() {
			var colName, dataType, isNullable, isPrimary string
			if err := rowsCols.Scan(&colName, &dataType, &isNullable, &isPrimary); err != nil {
				log.Printf("Error al escanear columna de %s: %v", tableName, err)
				continue
			}
			if colName == "id" || colName == "descripcion" || colName == "inactivo" {
				// Nothing ToDo
			} else {
				sbColumns.WriteString(colName + ",")
				intColums++
				sbColnums.WriteString(fmt.Sprintf("$%d,", intColums))
				sbUpdateColnums.WriteString("if(" + colName + "){ fields.push(`" + colName + " = $${idx++}`);values.push(" + colName + ");} ")
			}

			//			fmt.Fprintf(w, "%s\t%s\t%s\t%s\t%s\n", tableName, colName, dataType, isNullable, isPrimary)
			//fmt.Println("Campos ", tableName, colName, dataType, isNullable, isPrimary)
		}
		rowsCols.Close()

		getAllColums := sbColumns.String()
		numAllColums := sbColnums.String()
		getAllUpdateColums := sbUpdateColnums.String()

		getColums := getAllColums[:len(getAllColums)-1]
		numColums := numAllColums[:len(numAllColums)-1]

		sbTables.WriteString(tableName + ",")

		//fmt.Fprintln(w, "TABLA\tCAMPO\tTIPO\t¿NULO?\tCLAVE PRIMARIA")
		//fmt.Println("Tabla ", tableName)
		fmt.Fprintln(w, "// ******************* ")
		fmt.Fprintln(w, "// Rutas ", tableName)
		fmt.Fprintln(w, "// ******************* ")

		//		fmt.Fprintln(w, "GET /"+tableName+"")
		//		fmt.Fprintln(w, "GET /"+tableName+"/:id")
		//		fmt.Fprintln(w, "POST /"+tableName+"")
		//		fmt.Fprintln(w, "PUT /"+tableName+"/:id")
		//		fmt.Fprintln(w, "DEL /"+tableName+"/:id")
		//		fmt.Fprintln(w, "")

		fmt.Fprintln(w, " ")
		fmt.Fprintln(w, "console.log('GET /"+tableName+"');")
		fmt.Fprintln(w, "// GET /"+tableName+" - Obtener todos")
		fmt.Fprintln(w, "app.get('/"+tableName+"', async (req, res) => {")
		fmt.Fprintln(w, "try {")
		fmt.Fprintln(w, "		const result = await pool.query('SELECT * FROM "+tableName+" ORDER BY id');")
		fmt.Fprintln(w, "       if (result.rows.length === 0) {")
		fmt.Fprintln(w, "            return res.status(404).json({ error: 'No Existen Registros' });")
		fmt.Fprintln(w, "       } else {")
		fmt.Fprintln(w, "           return res.json(result.rows);")
		fmt.Fprintln(w, "       }")
		fmt.Fprintln(w, "	} catch (err) {")
		fmt.Fprintln(w, "		res.status(500).json({ error: 'Error al obtener registros', detalle: err.message });")
		fmt.Fprintln(w, "	}")
		fmt.Fprintln(w, "});")
		fmt.Fprintln(w, " ")

		fmt.Fprintln(w, "console.log('GET /"+tableName+"/:id');")
		fmt.Fprintln(w, "// GET /"+tableName+"/:id - Obtener uno por ID")
		fmt.Fprintln(w, "app.get('/"+tableName+"/:id', async (req, res) => {")
		fmt.Fprintln(w, "const id = parseInt(req.params.id);")
		fmt.Fprintln(w, "if (isNaN(id)) {")
		fmt.Fprintln(w, "    return res.status(400).json({ error: 'ID inválido' });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "  try {")
		fmt.Fprintln(w, "    const result = await pool.query('SELECT * FROM "+tableName+" WHERE id = $1', [id]);")
		fmt.Fprintln(w, "    if (result.rows.length === 0) {")
		fmt.Fprintln(w, "      return res.status(404).json({ error: 'Registro no encontrado' });")
		fmt.Fprintln(w, "    }")
		fmt.Fprintln(w, "    res.json(result.rows[0]);")
		fmt.Fprintln(w, "  } catch (err) {")
		fmt.Fprintln(w, "    res.status(500).json({ error: 'Error al obtener registro', detalle: err.message });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "});")
		fmt.Fprintln(w, " ")

		fmt.Fprintln(w, "console.log('POST /"+tableName+"')")
		fmt.Fprintln(w, "// POST /"+tableName+" - Crear un nuevo usuario")
		fmt.Fprintln(w, "app.post('/"+tableName+"', async (req, res) => {")
		fmt.Fprintln(w, "  const { "+getColums+" } = req.body;")
		fmt.Fprintln(w, "  //if (!nombre || !correo) {")
		fmt.Fprintln(w, "  //  return res.status(400).json({ error: 'Los campos  son requeridos' });")
		fmt.Fprintln(w, "  //}")
		fmt.Fprintln(w, "  try {")
		fmt.Fprintln(w, "    const result = await pool.query(")
		fmt.Fprintln(w, "      'INSERT INTO "+tableName+" ("+getColums+") VALUES ("+numColums+") RETURNING *',")
		fmt.Fprintln(w, "      ["+getColums+"]")
		fmt.Fprintln(w, "    );")
		fmt.Fprintln(w, "    res.status(201).json(result.rows[0]);")
		fmt.Fprintln(w, "  } catch (err) {")
		fmt.Fprintln(w, "    // Capturar posible violación de unicidad de email")
		fmt.Fprintln(w, "    if (err.code === '23505') { // código de violación de unique constraint en PostgreSQL")
		fmt.Fprintln(w, "      return res.status(409).json({ error: 'El Registro se Encuentra Duplicado' });")
		fmt.Fprintln(w, "    }")
		fmt.Fprintln(w, "    res.status(500).json({ error: 'Error al crear registro', detalle: err.message });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "});")
		fmt.Fprintln(w, " ")

		fmt.Fprintln(w, "console.log('PUT /"+tableName+"/:id')")
		fmt.Fprintln(w, "// PUT /"+tableName+"/:id - Actualizar un usuario existente")
		fmt.Fprintln(w, "app.put('/"+tableName+"/:id', async (req, res) => {")
		fmt.Fprintln(w, "  const id = parseInt(req.params.id);")
		fmt.Fprintln(w, "  if (isNaN(id)) {")
		fmt.Fprintln(w, "    return res.status(400).json({ error: 'ID inválido' });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "  const { "+getColums+" } = req.body;")
		fmt.Fprintln(w, "  //if (!nombre && !correo) {")
		fmt.Fprintln(w, "  //  return res.status(400).json({ error: 'Debe proporcionar al menos un campo para actualizar' });")
		fmt.Fprintln(w, "  //}")
		fmt.Fprintln(w, " ")
		fmt.Fprintln(w, "  // Construir dinámicamente la consulta de actualización")
		fmt.Fprintln(w, "  const fields = [];")
		fmt.Fprintln(w, "  const values = [];")
		fmt.Fprintln(w, "  let idx = 1;")
		fmt.Fprintln(w, "  "+getAllUpdateColums)

		//fmt.Fprintln(w, "  if (nombre) {")
		//fmt.Fprintln(w, "    fields.push(`nombre = $${idx++}`);")
		//fmt.Fprintln(w, "    values.push(nombre);")
		//fmt.Fprintln(w, "  }")
		//fmt.Fprintln(w, "  if (correo) {")
		//fmt.Fprintln(w, "    fields.push(`correo = $${idx++}`);")
		//fmt.Fprintln(w, "    values.push(correo);")
		//fmt.Fprintln(w, "  }")

		fmt.Fprintln(w, "  values.push(id); // para la cláusula WHERE")
		fmt.Fprintln(w, " ")
		fmt.Fprintln(w, "  const query = `UPDATE "+tableName+" SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`;")
		fmt.Fprintln(w, " ")
		fmt.Fprintln(w, "  try { ")
		fmt.Fprintln(w, "    const result = await pool.query(query, values);")
		fmt.Fprintln(w, "    if (result.rows.length === 0) {")
		fmt.Fprintln(w, "      return res.status(404).json({ error: 'Registro no encontrado' });")
		fmt.Fprintln(w, "    }")
		fmt.Fprintln(w, "    res.json(result.rows[0]);")
		fmt.Fprintln(w, "  } catch (err) {")
		fmt.Fprintln(w, "    if (err.code === '23505') {")
		fmt.Fprintln(w, "      return res.status(409).json({ error: 'Error al Actualizar, El Registro esta Duplicado' });")
		fmt.Fprintln(w, "    }")
		fmt.Fprintln(w, "    res.status(500).json({ error: 'Error al actualizar registro', detalle: err.message });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "});")
		fmt.Fprintln(w, " ")

		fmt.Fprintln(w, "console.log('DET /"+tableName+"/:id')")
		fmt.Fprintln(w, "// DELETE /"+tableName+"/:id - Eliminar un usuario")
		fmt.Fprintln(w, "app.delete('/"+tableName+"/:id', async (req, res) => {")
		fmt.Fprintln(w, "  const id = parseInt(req.params.id);")
		fmt.Fprintln(w, "  if (isNaN(id)) {")
		fmt.Fprintln(w, "    return res.status(400).json({ error: 'ID inválido' });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "  try {")
		fmt.Fprintln(w, "    const result = await pool.query('DELETE FROM "+tableName+" WHERE id = $1 RETURNING *', [id]);")
		fmt.Fprintln(w, "    if (result.rows.length === 0) {")
		fmt.Fprintln(w, "      return res.status(404).json({ error: 'Registro no encontrado' });")
		fmt.Fprintln(w, "    }")
		fmt.Fprintln(w, "    res.status(204).send(); // Sin contenido")
		fmt.Fprintln(w, "  } catch (err) {")
		fmt.Fprintln(w, "    res.status(500).json({ error: 'Error al eliminar registro', detalle: err.message });")
		fmt.Fprintln(w, "  }")
		fmt.Fprintln(w, "});")
		fmt.Fprintln(w, " ")

		fmt.Fprintln(w, "// ******************* ")
		fmt.Fprintln(w, " ")
		fmt.Fprintln(w, " ")

	} // end For

	// Asegurar que se escriban todos los datos
	w.Flush()

	resultadoTables := sbTables.String()
	resultadoAllTables := resultadoTables[:len(resultadoTables)-1]

	//runas := []rune(texto)

	//if len(runas) > 0 {
	// Cortar el slice de runas y volverlo a transformar en string
	//	resultado := string(runas[:len(runas)-1])

	fmt.Println("Información guardada en tablas.txt")
	fmt.Println(resultadoAllTables)
}
