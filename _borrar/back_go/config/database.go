// Paquete de configuracion de la Base de Datos
package config

import (
	"fmt"
	"go-postgres-api/models"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectDatabase() {
	// Reemplaza con tus credenciales de Postgres
	dsn := "host=localhost user=sdp password=sdp dbname=sdp port=5432 sslmode=disable TimeZone=America/Caracas"

	database, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Error al conectar a la base de datos: ", err)
	}

	// Ejecuta las migraciones automáticas (crea o actualiza la tabla)
	err = database.AutoMigrate(&models.User{})
	if err != nil {
		log.Fatal("Error en la migración: ", err)
	}

	fmt.Println("¡Conexión y migración exitosas con Postgres!")
	DB = database
}
