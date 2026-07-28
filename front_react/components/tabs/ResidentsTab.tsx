import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { useCondominio } from "@/context/CondominioContext";
import { toast } from "sonner";
import { CreditCard, Search, UserPlus, CheckCircle2 } from "lucide-react";

export default function ResidentsTab() {
  const { residents, payBalance } = useCondominio();
  const [search, setSearch] = useState("");
  const [payResident, setPayResident] = useState("");
  const [amount, setAmount] = useState("");
  const [method, setMethod] = useState("Tarjeta");

  const filtered = residents.filter(
    (r) => r.name.toLowerCase().includes(search.toLowerCase()) || r.apt.includes(search)
  );

  const handlePay = () => {
    const amt = parseFloat(amount);
    if (!amt || amt <= 0) {
      toast.error("Ingresa un monto válido");
      return;
    }
    const resident = residents.find((r) => r.id === payResident);
    if (!resident) return;
    payBalance(payResident, amt, method);
    toast.success(`Pago procesado para ${resident.name}`, {
      description: `$${amt} vía ${method} · Recibo generado`,
    });
    setPayResident("");
    setAmount("");
  };

  return (
    <Card className="border-purple-200/60 shadow-md">
      <CardHeader>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <CardTitle className="text-lg font-serif text-purple-900">Residentes y Saldos</CardTitle>
            <CardDescription>Gestiona los pagos de cuotas de cada apartamento</CardDescription>
          </div>
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-purple-400" />
            <Input
              placeholder="Buscar por nombre o apt..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 border-purple-200 focus:border-violet-400"
            />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {filtered.map((r) => (
            <div
              key={r.id}
              className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl bg-white border border-purple-100 hover:border-purple-300 hover:shadow-sm transition-all gap-3"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-400 to-purple-500 flex items-center justify-center text-white font-bold">
                  {r.apt}
                </div>
                <div>
                  <p className="font-medium text-purple-900">{r.name}</p>
                  <p className="text-xs text-purple-400">Apartamento {r.apt}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className={`text-lg font-bold ${r.balance > 0 ? "text-rose-600" : "text-emerald-600"}`}>
                    ${r.balance.toLocaleString()}
                  </p>
                  <p className="text-xs text-purple-400">
                    {r.balance > 0 ? "Saldo pendiente" : "Sin adeudo"}
                  </p>
                </div>
                {r.balance > 0 && (
                  <Button
                    onClick={() => setPayResident(r.id)}
                    size="sm"
                    className="bg-purple-600 hover:bg-purple-700 text-white"
                  >
                    <CreditCard className="w-4 h-4 mr-1" />
                    Pagar
                  </Button>
                )}
                {r.balance === 0 && (
                  <div className="flex items-center gap-1 text-emerald-500 text-sm">
                    <CheckCircle2 className="w-4 h-4" />
                    <span className="hidden sm:inline">Al día</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>

      <Dialog open={!!payResident} onOpenChange={(open) => !open && setPayResident("")}>
        <DialogContent className="bg-white">
          <DialogHeader>
            <DialogTitle className="font-serif text-purple-900">Procesar Pago</DialogTitle>
            <DialogDescription>
              {residents.find((r) => r.id === payResident)?.name} · Apto {residents.find((r) => r.id === payResident)?.apt}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div>
              <Label htmlFor="amount" className="text-purple-700">Monto a pagar</Label>
              <Input
                id="amount"
                type="number"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="mt-1 border-purple-200 focus:border-violet-400"
              />
            </div>
            <div>
              <Label className="text-purple-700">Método de pago</Label>
              <Select value={method} >
                <SelectTrigger className="mt-1 border-purple-200">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Tarjeta">Tarjeta de Crédito/Débito</SelectItem>
                  <SelectItem value="Transferencia">Transferencia Bancaria</SelectItem>
                  <SelectItem value="Efectivo">Efectivo</SelectItem>
                  <SelectItem value="PayPal">PayPal</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="p-3 rounded-lg bg-violet-50 border border-violet-100">
              <p className="text-xs text-purple-500">
                Al confirmar el pago, se generará un recibo digital automáticamente y se enviará al correo del residente.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setPayResident("")} className="border-purple-200">
              Cancelar
            </Button>
            <Button onClick={handlePay} className="bg-purple-600 hover:bg-purple-700 text-white">
              Confirmar Pago
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
}