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
public class PlanDeCuentas extends Incrementable4 {
	
    Integer ordenDelaCuenta;
	
	String numeroDeLaCuenta;

    String nombreDeLaCuenta;

    @ManyToOne(fetch=FetchType.LAZY, optional=false) // El propietario es obligatorio
    @DescriptionsList
//  @ReferenceView("Simple") // La vista llamada 'Simple' se usar� para visualizar esta referencia
    NivelDeCuentas nivel;

    @ManyToOne(fetch=FetchType.LAZY, optional=false) // El propietario es obligatorio
    @DescriptionsList
//  @ReferenceView("Simple") // La vista llamada 'Simple' se usar� para visualizar esta referencia
    TiposDeCuentas tipo;
    
}





