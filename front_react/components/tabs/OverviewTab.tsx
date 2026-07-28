import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCondominio } from "@/context/CondominioContext";
import { Building2, Users, CreditCard, Wrench, Clock, CheckCircle2, AlertCircle } from "lucide-react";

export default function OverviewTab() {
  const { residents, payments, expenses, maintenance } = useCondominio();

  const recentPayments = [...payments].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 5);
  const pendingMaint = maintenance.filter((m) => m.status !== "Resuelto");

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="border-purple-200/60 shadow-md">
        <CardHeader>
          <CardTitle className="text-lg font-serif text-purple-900 flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-violet-500" />
            Pagos Recientes
          </CardTitle>
          <CardDescription>Últimas transacciones registradas</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {recentPayments.length === 0 ? (
            <p className="text-sm text-purple-400 text-center py-6">No hay pagos registrados</p>
          ) : (
            recentPayments.map((p) => (
              <div key={p.id} className="flex items-center justify-between p-3 rounded-lg bg-violet-50/50 hover:bg-violet-100/60 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-purple-100 flex items-center justify-center text-purple-700 text-xs font-bold">
                    {p.apt}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-purple-900">{p.residentName}</p>
                    <p className="text-xs text-purple-400">{p.concept} · {p.method}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-emerald-600">+${p.amount}</p>
                  <p className="text-xs text-purple-400">{p.date}</p>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>

      <Card className="border-purple-200/60 shadow-md">
        <CardHeader>
          <CardTitle className="text-lg font-serif text-purple-900 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-violet-500" />
            Mantenimiento Pendiente
          </CardTitle>
          <CardDescription>Solicitudes de reparación activas</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {pendingMaint.length === 0 ? (
            <div className="flex flex-col items-center py-8 text-center">
              <CheckCircle2 className="w-10 h-10 text-emerald-400 mb-2" />
              <p className="text-sm text-purple-400">Todo al día. Sin pendientes.</p>
            </div>
          ) : (
            pendingMaint.map((m) => (
              <div key={m.id} className="flex items-start gap-3 p-3 rounded-lg bg-violet-50/50 hover:bg-violet-100/60 transition-colors">
                <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 ${
                  m.status === "Reportado" ? "bg-amber-100 text-amber-600" : "bg-blue-100 text-blue-600"
                }`}>
                  {m.status === "Reportado" ? <AlertCircle className="w-4 h-4" /> : <Clock className="w-4 h-4" />}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-purple-900">{m.area}</p>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      m.status === "Reportado" ? "bg-amber-100 text-amber-700" : "bg-blue-100 text-blue-700"
                    }`}>
                      {m.status}
                    </span>
                  </div>
                  <p className="text-xs text-purple-400 mt-0.5">{m.description}</p>
                  <p className="text-xs text-purple-300 mt-1">Apto {m.apt} · {m.date}</p>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>

      <Card className="border-purple-200/60 shadow-md lg:col-span-2">
        <CardHeader>
          <CardTitle className="text-lg font-serif text-purple-900 flex items-center gap-2">
            <Users className="w-5 h-5 text-violet-500" />
            Estado de Cuentas de Residentes
          </CardTitle>
          <CardDescription>Resumen de saldos por apartamento</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {residents.map((r) => (
              <div key={r.id} className={`p-4 rounded-xl border-2 transition-all hover:shadow-sm ${
                r.balance > 0
                  ? "border-rose-200 bg-rose-50/50"
                  : "border-emerald-200 bg-emerald-50/50"
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-bold text-purple-900">Apto {r.apt}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    r.balance > 0 ? "bg-rose-200 text-rose-700" : "bg-emerald-200 text-emerald-700"
                  }`}>
                    {r.balance > 0 ? "Pendiente" : "Al día"}
                  </span>
                </div>
                <p className="text-sm text-purple-700">{r.name}</p>
                <p className={`text-lg font-bold mt-1 ${r.balance > 0 ? "text-rose-600" : "text-emerald-600"}`}>
                  ${r.balance.toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}