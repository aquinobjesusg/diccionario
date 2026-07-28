import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { useCondominio } from "@/context/CondominioContext";
import { toast } from "sonner";
import { Plus, Receipt, Trash2 } from "lucide-react";

export default function ExpensesTab() {
  const { expenses, addExpense } = useCondominio();
  const [open, setOpen] = useState(false);
  const [concept, setConcept] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("Servicios");

  const handleAdd = () => {
    const amt = parseFloat(amount);
    if (!concept || !amt || amt <= 0) {
      toast.error("Completa todos los campos");
      return;
    }
    addExpense({
      concept,
      amount: amt,
      date: new Date().toISOString().split("T")[0],
      category,
    });
    toast.success("Recibo de gasto emitido", { description: `${concept} · $${amt}` });
    setOpen(false);
    setConcept("");
    setAmount("");
  };

  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  const byCategory = expenses.reduce((acc, e) => {
    acc[e.category] = (acc[e.category] || 0) + e.amount;
    return acc;
  }, {} as Record<string, number>);

  const categoryColors: Record<string, string> = {
    "Servicios": "bg-blue-100 text-blue-700",
    "Mantenimiento": "bg-amber-100 text-amber-700",
    "Personal": "bg-violet-100 text-violet-700",
    "Otros": "bg-slate-100 text-slate-700",
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="border-purple-200/60 shadow-md lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-lg font-serif text-purple-900">Recibos de Gastos</CardTitle>
                <CardDescription>Gastos del condominio por categoría</CardDescription>
              </div>
              <Button onClick={() => setOpen(true)} className="bg-purple-600 hover:bg-purple-700 text-white">
                <Plus className="w-4 h-4 mr-1" />
                Nuevo Gasto
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {expenses.map((e) => (
                <div key={e.id} className="flex items-center justify-between p-3 rounded-lg bg-violet-50/40 hover:bg-violet-100/50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center">
                      <Receipt className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-purple-900">{e.concept}</p>
                      <p className="text-xs text-purple-400">{e.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${categoryColors[e.category] || categoryColors["Otros"]}`}>
                      {e.category}
                    </span>
                    <span className="text-sm font-bold text-purple-900">${e.amount.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-200/60 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg font-serif text-purple-900">Resumen</CardTitle>
            <CardDescription>Distribución de gastos</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 rounded-xl bg-gradient-to-br from-purple-600 to-violet-600 text-white">
              <p className="text-xs uppercase tracking-wide text-purple-200">Total Gastos</p>
              <p className="text-3xl font-bold mt-1">${total.toLocaleString()}</p>
            </div>
            <div className="space-y-2">
              {Object.entries(byCategory).map(([cat, amt]) => (
                <div key={cat} className="flex items-center justify-between p-2 rounded-lg bg-violet-50/50">
                  <span className={`text-xs px-2 py-1 rounded-full ${categoryColors[cat] || categoryColors["Otros"]}`}>
                    {cat}
                  </span>
                  <span className="text-sm font-semibold text-purple-900">${amt.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="bg-white">
          <DialogHeader>
            <DialogTitle className="font-serif text-purple-900">Emitir Recibo de Gasto</DialogTitle>
            <DialogDescription>Registra un nuevo gasto del condominio</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div>
              <Label htmlFor="concept" className="text-purple-700">Concepto</Label>
              <Input
                id="concept"
                placeholder="Ej: Luz - Áreas comunes"
                value={concept}
                onChange={(e) => setConcept(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
            <div>
              <Label htmlFor="amount2" className="text-purple-700">Monto</Label>
              <Input
                id="amount2"
                type="number"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
            <div>
              <Label className="text-purple-700">Categoría</Label>
              <Select value={category} >
                <SelectTrigger className="mt-1 border-purple-200">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Servicios">Servicios</SelectItem>
                  <SelectItem value="Mantenimiento">Mantenimiento</SelectItem>
                  <SelectItem value="Personal">Personal</SelectItem>
                  <SelectItem value="Otros">Otros</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)} className="border-purple-200">
              Cancelar
            </Button>
            <Button onClick={handleAdd} className="bg-purple-600 hover:bg-purple-700 text-white">
              Emitir Recibo
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}