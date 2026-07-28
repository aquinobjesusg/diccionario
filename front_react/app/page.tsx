'use client'

import { useEffect, useState, useCallback } from "react";
import { Plus, Pencil, Trash2, Mail, User, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { toast } from "sonner";

interface Usuario {
  id?: number;
  nombre: string;
  correo: string;
}

type EstadoFormulario = "crear" | "editar";

const API_URL = "http://localhost:8080/usuarios";


export default function Home() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [errorCarga, setErrorCarga] = useState<string | null>(null);

  const [dialogoFormAbierto, setDialogoFormAbierto] = useState(false);
  const [estadoForm, setEstadoForm] = useState<EstadoFormulario>("crear");
  const [formulario, setFormulario] = useState<Usuario>({ nombre: "", correo: "" });
  const [enviando, setEnviando] = useState(false);

  const [usuarioAEliminar, setUsuarioAEliminar] = useState<Usuario | null>(null);
  const [eliminando, setEliminando] = useState(false);

  const cargarUsuarios = useCallback(async () => {
    setCargando(true);
    setErrorCarga(null);
    try {
      const res = await fetch(API_URL);
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setUsuarios(Array.isArray(data) ? data : []);
    } catch (err) {
      setErrorCarga("No se pudo conectar con el servidor. Mostrando datos locales de demostración.");
      setUsuarios([
        { id: 1, nombre: "Ana García", correo: "ana.garcia@example.com" },
        { id: 2, nombre: "Bruno López", correo: "bruno.lopez@example.com" },
        { id: 3, nombre: "Carla Méndez", correo: "carla.mendez@example.com" },
      ]);
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarUsuarios();
  }, [cargarUsuarios]);

  const abrirCrear = () => {
    setEstadoForm("crear");
    setFormulario({ nombre: "", correo: "" });
    setDialogoFormAbierto(true);
  };

  const abrirEditar = (usuario: Usuario) => {
    setEstadoForm("editar");
    setFormulario({ id: usuario.id, nombre: usuario.nombre, correo: usuario.correo });
    setDialogoFormAbierto(true);
  };

  const validar = (): string | null => {
    if (!formulario.nombre.trim()) return "El nombre es obligatorio.";
    if (!formulario.correo.trim()) return "El correo es obligatorio.";
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(formulario.correo)) return "El correo no tiene un formato válido.";
    return null;
  };

  const guardar = async () => {
    const error = validar();
    if (error) {
      toast.error(error);
      return;
    }
    setEnviando(true);
    try {
      const metodo = estadoForm === "crear" ? "POST" : "PUT";
      const url = estadoForm === "crear" ? API_URL : `${API_URL}/${formulario.id}`;
      const res = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre: formulario.nombre, correo: formulario.correo }),
      });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      toast.success(estadoForm === "crear" ? "Usuario creado con éxito." : "Usuario actualizado con éxito.");
      setDialogoFormAbierto(false);
      await cargarUsuarios();
    } catch {
      toast.error("Ocurrió un error al guardar el usuario.");
    } finally {
      setEnviando(false);
    }
  };

  const confirmarEliminar = async () => {
    if (!usuarioAEliminar?.id) return;
    setEliminando(true);
    try {
      const res = await fetch(`${API_URL}/${usuarioAEliminar.id}`, { method: "DELETE" });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      toast.success("Usuario eliminado con éxito.");
      setUsuarioAEliminar(null);
      await cargarUsuarios();
    } catch {
      toast.error("Ocurrió un error al eliminar el usuario.");
    } finally {
      setEliminando(false);
    }
  };

  const iniciales = (nombre: string) =>
    nombre
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((p) => p[0]?.toUpperCase() ?? "")
      .join("");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Banda superior con degradado teal */}
      <header className="bg-gradient-to-r from-teal-700 via-teal-600 to-emerald-600 px-6 py-10 sm:px-10 sm:py-14 shadow-md">
        <div className="mx-auto max-w-5xl">
          <p className="text-teal-100 text-sm font-medium tracking-wide uppercase">Administración</p>
          <h1 className="mt-1 font-serif text-3xl sm:text-4xl font-bold text-white">
            Gestión de Usuarios
          </h1>
          <p className="mt-2 text-teal-50/90 max-w-2xl">
            Crea, edita y elimina los registros de usuarios conectados al servicio REST.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 sm:px-6 -mt-6 pb-16">
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
          {/* Barra de acciones */}
          <div className="flex items-center justify-between gap-4 px-6 py-5 border-b border-slate-100 bg-slate-50/60">
            <div>
              <h2 className="text-lg font-semibold text-slate-800">Listado de usuarios</h2>
              <p className="text-sm text-slate-500">
                {cargando ? "Cargando…" : `${usuarios.length} registro${usuarios.length === 1 ? "" : "s"} en total`}
              </p>
            </div>
            <Button
              onClick={abrirCrear}
              className="bg-teal-600 hover:bg-teal-700 text-white rounded-xl shadow-sm"
            >
              <Plus className="size-4 mr-1.5" />
              Nuevo usuario
            </Button>
          </div>

          {/* Tabla */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500 border-b border-slate-100 bg-slate-50/40">
                  <th className="px-6 py-3 font-medium">Usuario</th>
                  <th className="px-6 py-3 font-medium hidden sm:table-cell">ID</th>
                  <th className="px-6 py-3 font-medium">Correo electrónico</th>
                  <th className="px-6 py-3 font-medium text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {cargando && (
                  <tr>
                    <td colSpan={4} className="px-6 py-16 text-center text-slate-500">
                      <Loader2 className="size-6 mx-auto mb-3 animate-spin text-teal-600" />
                      Cargando usuarios…
                    </td>
                  </tr>
                )}

                {!cargando && usuarios.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-6 py-16 text-center">
                      <div className="flex flex-col items-center gap-3 text-slate-500">
                        <div className="size-12 rounded-full bg-slate-100 flex items-center justify-center">
                          <User className="size-6 text-slate-400" />
                        </div>
                        <p className="font-medium text-slate-700">No hay usuarios registrados</p>
                        <p className="text-sm">Crea tu primer usuario usando el botón superior.</p>
                      </div>
                    </td>
                  </tr>
                )}

                {!cargando &&
                  usuarios.map((u) => (
                    <tr
                      key={u.id ?? u.correo}
                      className="border-b border-slate-50 last:border-0 hover:bg-teal-50/40 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="size-10 rounded-full bg-gradient-to-br from-teal-500 to-emerald-500 text-white flex items-center justify-center font-semibold text-sm shadow-sm">
                            {iniciales(u.nombre) || "?"}
                          </div>
                          <span className="font-medium text-slate-800">{u.nombre}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 hidden sm:table-cell">
                        <span className="inline-flex items-center rounded-md bg-slate-100 px-2 py-1 text-xs font-mono text-slate-600">
                          #{u.id}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2 text-slate-600">
                          <Mail className="size-4 text-slate-400 shrink-0" />
                          <span className="truncate">{u.correo}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center justify-end gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => abrirEditar(u)}
                            className="rounded-lg border-slate-200 hover:border-teal-400 hover:text-teal-700 hover:bg-teal-50"
                          >
                            <Pencil className="size-3.5 mr-1" />
                            <span className="hidden sm:inline">Editar</span>
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setUsuarioAEliminar(u)}
                            className="rounded-lg border-slate-200 text-rose-600 hover:text-rose-700 hover:border-rose-300 hover:bg-rose-50"
                          >
                            <Trash2 className="size-3.5 mr-1" />
                            <span className="hidden sm:inline">Eliminar</span>
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {errorCarga && (
          <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
            {errorCarga}
          </div>
        )}
      </main>

      {/* Dialogo Crear / Editar */}
      <Dialog open={dialogoFormAbierto} onOpenChange={setDialogoFormAbierto}>
        <DialogContent className="sm:max-w-md rounded-2xl">
          <DialogHeader>
            <DialogTitle className="font-serif text-xl">
              {estadoForm === "crear" ? "Nuevo usuario" : "Editar usuario"}
            </DialogTitle>
            <DialogDescription>
              {estadoForm === "crear"
                ? "Completa los datos para registrar un nuevo usuario."
                : "Modifica la información del usuario seleccionado."}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            <div className="space-y-2">
              <Label htmlFor="nombre" className="text-slate-700">Nombre completo</Label>
              <Input
                id="nombre"
                value={formulario.nombre}
                onChange={(e) => setFormulario((f) => ({ ...f, nombre: e.target.value }))}
                placeholder="Ej. María Fernández"
                className="rounded-lg"
                autoFocus
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="correo" className="text-slate-700">Correo electrónico</Label>
              <Input
                id="correo"
                type="email"
                value={formulario.correo}
                onChange={(e) => setFormulario((f) => ({ ...f, correo: e.target.value }))}
                placeholder="Ej. maria@example.com"
                className="rounded-lg"
              />
            </div>
          </div>

          <DialogFooter className="gap-2">
            <Button
              variant="outline"
              onClick={() => setDialogoFormAbierto(false)}
              disabled={enviando}
              className="rounded-lg"
            >
              Cancelar
            </Button>
            <Button
              onClick={guardar}
              disabled={enviando}
              className="bg-teal-600 hover:bg-teal-700 text-white rounded-lg"
            >
              {enviando && <Loader2 className="size-4 mr-2 animate-spin" />}
              {estadoForm === "crear" ? "Crear usuario" : "Guardar cambios"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Dialogo de confirmación de eliminación */}
      <AlertDialog open={!!usuarioAEliminar} onOpenChange={(open) => !open && setUsuarioAEliminar(null)}>
        <AlertDialogContent className="rounded-2xl">
          <AlertDialogHeader>
            <AlertDialogTitle className="font-serif text-xl">¿Eliminar usuario?</AlertDialogTitle>
            <AlertDialogDescription>
              Se eliminará permanentemente a{" "}
              <span className="font-semibold text-slate-800">{usuarioAEliminar?.nombre}</span> y su correo{" "}
              <span className="font-semibold text-slate-800">{usuarioAEliminar?.correo}</span>. Esta acción no se puede deshacer.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="gap-2">
            <AlertDialogCancel className="rounded-lg" disabled={eliminando}>
              Cancelar
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmarEliminar}
              disabled={eliminando}
              className="bg-rose-600 hover:bg-rose-700 text-white rounded-lg"
            >
              {eliminando && <Loader2 className="size-4 mr-2 animate-spin" />}
              Sí, eliminar
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
