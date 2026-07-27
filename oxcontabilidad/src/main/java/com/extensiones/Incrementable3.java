package com.extensiones;
 
import javax.persistence.*;

import org.openxava.annotations.*;

import lombok.*;
 
@MappedSuperclass // Marcada como una superclase mapeada en vez de como una entidad
@Getter @Setter
public class Incrementable3 {
 
	@Id @ReadOnly @Hidden
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private Integer id;
	
    @Column(length=255) // La longitud de columna se usa a nivel UI y a nivel DB
    @Required  // Se mostrar� un error de validaci�n si la propiedad nombre se deja en blanco
    String descripcion;

    @Column(length=20) // La longitud de columna se usa a nivel UI y a nivel DB
    //@Required  // Se mostrará un error de validación si la propiedad nombre se deja en blanco
    String siglas;
    
    
}