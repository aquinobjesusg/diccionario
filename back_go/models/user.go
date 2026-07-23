package models

import "gorm.io/gorm"

type User struct {
	gorm.Model        // Agrega ID, CreatedAt, UpdatedAt, DeletedAt automáticamente
	nombre     string `gorm:"size:100;not null" json:"name"`
	correo     string `gorm:"uniqueIndex;size:100;not null" json:"email"`
}
