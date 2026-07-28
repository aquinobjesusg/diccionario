import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { useCondominio } from "@/context/CondominioContext";
import { toast } from "sonner";
import { Plus, Wrench, AlertCircle, Clock, CheckCircle2 } from "lucide-react";

export default function MaintenanceTab() {
  const { maintenance, addMaintenance, updateMaintenance } = useCondominio();
  const [open, setOpen] = useState(false);
  const [area, setArea] = useState("");
  const [description, setDescription] = useState("");
  const [apt, setApt] = useState("");

  const handleAdd = () => {
    if (!area || !description || !apt) {
      toast.error("Completa todos los campos");
      return;
    }
    addMaintenance({
      area,
      description,
      status: "Reportado",
      date: new Date().toISOString().split("T")[0],
      apt,
    });
    toast.success("Solicitud registrada", { description: `${area} - Apto ${apt}` });
    setOpen(false);
    setArea("");
    setDescription("");
    setApt("");
  };

  const statusConfig = {
    "Reportado": { icon: AlertCircle, color: "bg-amber-100 text-amber-600", badge: "bg-amber-200 text-amber-700" },
    "En Proceso": { icon: Clock, color: "bg-blue-100 text-blue-600", badge: "bg-blue-200 text-blue-700" },
    "Resuelto": { icon: CheckCircle2, color: "bg-emerald-100 text-emerald-600", badge: "bg-emerald-200 text-emerald-700" },
  };

  return (
    <Card className="border-purple-200/60 shadow-md">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg font-serif text-purple-900">Solicitudes de Mantenimiento</CardTitle>
            <CardDescription>Gestiona reparaciones y mejoras del condominio</CardDescription>
          </div>
          <Button onClick={() => setOpen(true)} className="bg-purple-600 hover:bg-purple-700 text-white">
            <Plus className="w-4 h-4 mr-1" />
            Nueva Solicitud
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {maintenance.map((m) => {
            const config = statusConfig[m.status];
            const Icon = config.icon;
            return (
              <div key={m.id} className="p-4 rounded-xl bg-white border-2 border-purple-100 hover:border-purple-300 hover:shadow-sm transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${config.color}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <p className="font-medium text-purple-900">{m.area}</p>
                      <p className="text-xs text-purple-400">Apto {m.apt} · {m.date}</p>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${config.badge}`}>
                    {m.status}
                  </span>
                </div>
                <p className="text-sm text-purple-600 mb-3">{m.description}</p>
                <div className="flex gap-2">
                  {m.status !== "En Proceso" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        updateMaintenance(m.id, "En Proceso");
                        toast.info("Estado actualizado: En Proceso");
                      }}
                      className="text-xs border-blue-200 text-blue-600 hover:bg-blue-50"
                    >
                      Marcar en proceso
                    </Button>
                  )}
                  {m.status !== "Resuelto" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        updateMaintenance(m.id, "Resuelto");
                        toast.success("Mantenimiento resuelto");
                      }}
                      className="text-xs border-emerald-200 text-emerald-600 hover:bg-emerald-50"
                    >
                      Marcar resuelto
                    </Button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="bg-white">
          <DialogHeader>
            <DialogTitle className="font-serif text-purple-900">Nueva Solicitud de Mantenimiento</DialogTitle>
            <DialogDescription>Registra una nueva solicitud de reparación</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div>
              <Label htmlFor="area" className="text-purple-700">Área / Tipo</Label>
              <Input
                id="area"
                placeholder="Ej: Ascensor, Plomería, Electricidad"
                value={area}
                onChange={(e) => setArea(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
            <div>
              <Label htmlFor="apt" className="text-purple-700">Apartamento</Label>
              <Input
                id="apt"
                placeholder="Ej: 101"
                value={apt}
                onChange={(e) => setApt(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
            <div>
              <Label htmlFor="desc" className="text-purple-700">Descripción</Label>
              <Textarea
                id="desc"
                placeholder="Describe el problema..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)} className="border-purple-200">
              Cancelar
            </Button>
            <Button onClick={handleAdd} className="bg-purple-600 hover:bg-purple-700 text-white">
              Registrar Solicitud
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
}