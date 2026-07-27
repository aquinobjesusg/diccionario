package controllers

import (
	"go-postgres-api/config"
	"go-postgres-api/models"
	"net/http"

	"github.com/gin-gonic/gin"
)

// CreateUser guarda un nuevo usuario en Postgres
func Create(c *gin.Context) {
	var input models.Roles

	// Valida que el JSON recibido coincida con la estructura
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Inserta en la base de datos usando GORM
	if err := config.DB.Create(&input).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo crear el usuario"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"message": "Usuario creado exitosamente",
		"user":    input,
	})
}

// GetUsers obtiene todos los usuarios
func Get(c *gin.Context) {
	var users []models.Roles

	if err := config.DB.Find(&users).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener los usuarios"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"users": users,
		"count": len(users),
	})
}

// GetUserByID obtiene un usuario por ID
func GetByID(c *gin.Context) {
	id := c.Param("id")
	var user models.Roles

	if err := config.DB.First(&user, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuario no encontrado"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"user": user})
}

// UpdateUser actualiza un usuario existente
func Update(c *gin.Context) {
	id := c.Param("id")
	var user models.Roles

	// Buscar el usuario
	if err := config.DB.First(&user, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuario no encontrado"})
		return
	}

	// Validar los datos de entrada
	var input models.Roles
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Actualizar el usuario
	if err := config.DB.Model(&user).Updates(input).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo actualizar el usuario"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Usuario actualizado exitosamente",
		"user":    user,
	})
}

// DeleteUser elimina un usuario
func Delete(c *gin.Context) {
	id := c.Param("id")

	if err := config.DB.Delete(&models.Roles{}, id).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo eliminar el usuario"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Usuario eliminado exitosamente"})
}
