package com.extensiones;
 
import javax.persistence.*;

import org.openxava.annotations.*;

import lombok.*;
 
@MappedSuperclass // Marcada como una superclase mapeada en vez de como una entidad
@Getter @Setter
public class Incrementable {
 
	@Id @Hidden
	@ReadOnly
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private Integer id;
	
}