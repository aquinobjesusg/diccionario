En resumen: identificar si los paquetes están instalados, si el alias funciona, y si los componentes existen. Además, verificar que el archivo donde se importa tenga la extensión correcta (.jsx, .tsx) y que el entorno soporte JSX.

Proporcionaré pasos concretos:

Instalar dependencias:

bash
npm install sonner framer-motion lucide-react
Y para shadcn/ui, necesita instalar y configurar shadcn, luego agregar componentes.

Configurar alias @:

En vite.config.ts:

ts
import path from "path";
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
En tsconfig.json:

json
"compilerOptions": {
  "baseUrl": ".",
  "paths": {
    "@/*": ["./src/*"]
  }
}
(Para Next.js, similar en tsconfig.json y jsconfig.json).

Si usa shadcn/ui, asegurarse de haber ejecutado:

bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input label
Verificar que los archivos de componentes existen en src/components/ui/button.tsx, etc.

También recordar que si el error es de tipo (TypeScript), puede ser que no tenga los tipos de esos paquetes, pero normalmente vienen incluidos.

Si el error es "Cannot find module", es porque no está instalado o el path no resuelve.

También podría ser que el proyecto no tenga soporte para JSX, pero eso sería un error de sintaxis.

Finalmente, dar un consejo para depurar: mirar el mensaje de error exacto.

Voy a escribir una respuesta clara, paso a paso, y alentadora.

El problema con esas importaciones suele deberse a una de estas tres causas:

Paquetes no instalados – sonner, framer-motion, lucide-react y los componentes de @/components/ui/… no están disponibles en node_modules.

Alias de ruta @ no configurado – el proyecto no sabe que @/ apunta a la carpeta src/.

Componentes de shadcn/ui no generados – los archivos button.tsx, input.tsx, label.tsx no existen en src/components/ui/.

🔧 Solución paso a paso
1. Instala las dependencias faltantes
bash
npm install sonner framer-motion lucide-react
(Si usas yarn o pnpm, usa el comando correspondiente).

2. Configura el alias @
Dependiendo de tu bundler:

Vite (vite.config.ts)
ts
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
Next.js (tsconfig.json o jsconfig.json)
json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
Create React App (sin eject)
No soporta alias nativamente. Puedes usar craco o react-app-rewired, o cambiar las importaciones a rutas relativas (ej. ../../components/ui/button).

3. Agrega los componentes de shadcn/ui
Si estás usando shadcn/ui, debes inicializarlo y añadir los componentes:

bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input label
Esto creará los archivos en src/components/ui/ y los registrará en components.json.

Si no usas shadcn/ui, deberás crear esos componentes manualmente o cambiar las importaciones a tus propios componentes.

4. Reinicia el servidor de desarrollo
Después de instalar y configurar, detén el servidor (Ctrl+C) y vuelve a ejecutar npm run dev (o el comando que uses) para que los cambios surtan efecto.