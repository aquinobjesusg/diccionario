package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
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
	fmt.Fprintln(w, "TABLA\tCAMPO\tTIPO\t¿NULO?\tCLAVE PRIMARIA")

	// Recorrer cada tabla
	for rowsTables.Next() {
		var tableName string
		if err := rowsTables.Scan(&tableName); err != nil {
			log.Fatal("Error al escanear tabla: ", err)
		}

		fmt.Println("Tabla ", tableName)

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

		// Escribir cada columna
		for rowsCols.Next() {
			var colName, dataType, isNullable, isPrimary string
			if err := rowsCols.Scan(&colName, &dataType, &isNullable, &isPrimary); err != nil {
				log.Printf("Error al escanear columna de %s: %v", tableName, err)
				continue
			}
			fmt.Fprintf(w, "%s\t%s\t%s\t%s\t%s\n", tableName, colName, dataType, isNullable, isPrimary)
			fmt.Println("Campos ", tableName, colName, dataType, isNullable, isPrimary)
		}
		rowsCols.Close()
	}

	// Asegurar que se escriban todos los datos
	w.Flush()

	fmt.Println("Información guardada en tablas.txt")
}
