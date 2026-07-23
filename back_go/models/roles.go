package models

import "gorm.io/gorm"

type Roles struct {
	gorm.Model        // Agrega ID, CreatedAt, UpdatedAt, DeletedAt automáticamente
	nombre     string `gorm:"uniqueIndex;size:255;not null" json:"nombre"`
}
