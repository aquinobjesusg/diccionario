# Instrucciones
- Instalar GoLand

- Ejecuta la Instruccion
go run main.go

- Utilizar las Siguientes URLS
http://localhost:8080/users
http://localhost:8080/users/:id


KWw&LRw%^6eYF1T=






# Crear el directorio del proyecto
mkdir go-postgres-api
cd go-postgres-api

# Inicializar el módulo Go
go mod init go-postgres-api

# Instalar las dependencias necesarias (corregido)
go get -u github.com/lib/pq
go get -u gorm.io/gorm
go get -u gorm.io/driver/postgres
go get -u github.com/gin-contrib/cors

// http://localhost:8080/users
// http://localhost:8080/users/:id

// main.go
package main

import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
)

type User struct {
    ID    uint   `gorm:"primaryKey"`
    Name  string `gorm:"size:100"`
    Email string `gorm:"uniqueIndex;size:100"`
}

func main() {
    dsn := "host=localhost user=postgres password=yourpassword dbname=yourdb port=5432 sslmode=disable"
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("Failed to connect to database")
    }

    // Migrar el esquema
    db.AutoMigrate(&User{})
}


from origin 'null' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.


header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: access");
header("Access-Control-Allow-Methods: GET,POST");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
