package com.contabilidad;
 
import javax.persistence.*;

import org.openxava.annotations.*;

import com.extensiones.*;

import lombok.*;

@Entity @Getter @Setter
@View(name="Simple", // Esta vista solo se usarÃ¡ cuando se especifique âSimpleâ
members="id, descripcion" // Muestra Ãºnicamente numero y nombre en la misma lÃ­nea
)
@Tab(properties="ordenDelaCuenta, numeroDeLaCuenta, nombreDeLaCuenta,  nivel.descripcion, tipo.descripcion") // Tab sin nombre, es el de por defecto
public class OperacionesGeneradas extends Incrementable4 {
	
    Integer numeroDeOperacion;
	
	String numeroDeLaCuenta;
	
	String descripcionOperacion;

	Double montoDebe;
	
	Double montoHaber;
	
	Double diferencia;
    
}





