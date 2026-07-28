import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useCondominio } from "@/context/CondominioContext";
import { toast } from "sonner";
import { Download, Search, FileText, Filter } from "lucide-react";

export default function PaymentsTab() {
  const { payments } = useCondominio();
  const [search, setSearch] = useState("");
  const [filterMethod, setFilterMethod] = useState("all");

  const filtered = payments
    .filter((p) => filterMethod === "all" || p.method === filterMethod)
    .filter((p) => p.residentName.toLowerCase().includes(search.toLowerCase()) || p.apt.includes(search))
    .sort((a, b) => b.date.localeCompare(a.date));

  const downloadReceipt = (payment: typeof payments[0]) => {
    const receiptContent = `
      RECIBO DE PAGO - CONDOMINIO
      ============================
      
      N° de Recibo: ${payment.id.toUpperCase()}
      Fecha: ${payment.date}
      
      Residente: ${payment.residentName}
      Apartamento: ${payment.apt}
      
      Concepto: ${payment.concept}
      Método de Pago: ${payment.method}
      
      Monto: $${payment.amount.toLocaleString()}
      Estado: ${payment.status}
      
      ============================
      Gracias por su pago puntual.
    `.trim();

    const blob = new Blob([receiptContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `recibo-${payment.apt}-${payment.date}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Recibo descargado", { description: `Recibo ${payment.id} generado correctamente` });
  };

  return (
    <Card className="border-purple-200/60 shadow-md">
      <CardHeader>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <CardTitle className="text-lg font-serif text-purple-900">Historial de Pagos</CardTitle>
            <CardDescription>Emite y descarga recibos de todas las transacciones</CardDescription>
          </div>
          <div className="flex gap-2">
            <div className="relative flex-1 sm:w-48">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-purple-400" />
              <Input
                placeholder="Buscar..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 border-purple-200 focus:border-violet-400"
              />
            </div>
            <Select value={filterMethod} >
              <SelectTrigger className="w-36 border-purple-200">
                <div className="flex items-center gap-2">
                  <Filter className="w-3.5 h-3.5 text-purple-400" />
                  <SelectValue />
                </div>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos</SelectItem>
                <SelectItem value="Tarjeta">Tarjeta</SelectItem>
                <SelectItem value="Transferencia">Transferencia</SelectItem>
                <SelectItem value="Efectivo">Efectivo</SelectItem>
                <SelectItem value="PayPal">PayPal</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center py-12 text-center">
            <FileText className="w-12 h-12 text-purple-200 mb-3" />
            <p className="text-sm text-purple-400">No se encontraron pagos</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-purple-100">
                  <th className="text-left py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide">Recibo</th>
                  <th className="text-left py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide">Residente</th>
                  <th className="text-left py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide hidden sm:table-cell">Concepto</th>
                  <th className="text-left py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide">Método</th>
                  <th className="text-left py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide hidden md:table-cell">Fecha</th>
                  <th className="text-right py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide">Monto</th>
                  <th className="text-right py-3 px-2 text-xs font-semibold text-purple-400 uppercase tracking-wide">Acción</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((p) => (
                  <tr key={p.id} className="border-b border-purple-50 hover:bg-violet-50/40 transition-colors">
                    <td className="py-3 px-2">
                      <span className="text-xs font-mono text-purple-500">{p.id.toUpperCase()}</span>
                    </td>
                    <td className="py-3 px-2">
                      <p className="text-sm font-medium text-purple-900">{p.residentName}</p>
                      <p className="text-xs text-purple-400">Apto {p.apt}</p>
                    </td>
                    <td className="py-3 px-2 hidden sm:table-cell">
                      <span className="text-sm text-purple-600">{p.concept}</span>
                    </td>
                    <td className="py-3 px-2">
                      <span className="text-xs px-2 py-1 rounded-full bg-violet-100 text-violet-700">{p.method}</span>
                    </td>
                    <td className="py-3 px-2 hidden md:table-cell">
                      <span className="text-sm text-purple-500">{p.date}</span>
                    </td>
                    <td className="py-3 px-2 text-right">
                      <span className="text-sm font-bold text-emerald-600">${p.amount.toLocaleString()}</span>
                    </td>
                    <td className="py-3 px-2 text-right">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadReceipt(p)}
                        className="text-purple-600 hover:bg-purple-100"
                      >
                        <Download className="w-4 h-4" />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}