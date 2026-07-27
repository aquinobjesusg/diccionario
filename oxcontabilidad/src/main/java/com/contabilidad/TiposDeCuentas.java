package com.contabilidad;
 
import javax.persistence.*;

import org.openxava.annotations.*;

import com.extensiones.*;

import lombok.*;

@Entity @Getter @Setter
@View(name="Simple", // Esta vista solo se usarÃ¡ cuando se especifique âSimpleâ
members="id, descripcion" // Muestra Ãºnicamente numero y nombre en la misma lÃ­nea
)
public class TiposDeCuentas extends Incrementable2 {
	
    
}





