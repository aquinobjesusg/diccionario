import { createContext, useContext, useState, ReactNode } from "react";

export interface Resident {
  id: string;
  name: string;
  apt: string;
  balance: number;
}

export interface Payment {
  id: string;
  residentId: string;
  residentName: string;
  apt: string;
  amount: number;
  date: string;
  method: string;
  concept: string;
  status: "Completado" | "Pendiente";
}

export interface Expense {
  id: string;
  concept: string;
  amount: number;
  date: string;
  category: string;
}

export interface Maintenance {
  id: string;
  area: string;
  description: string;
  status: "Reportado" | "En Proceso" | "Resuelto";
  date: string;
  apt: string;
}

interface CondominioContextType {
  residents: Resident[];
  payments: Payment[];
  expenses: Expense[];
  maintenance: Maintenance[];
  addPayment: (p: Omit<Payment, "id">) => void;
  addExpense: (e: Omit<Expense, "id">) => void;
  addMaintenance: (m: Omit<Maintenance, "id">) => void;
  updateMaintenance: (id: string, status: Maintenance["status"]) => void;
  payBalance: (residentId: string, amount: number, method: string) => void;
}

const CondominioContext = createContext<CondominioContextType | undefined>(undefined);

export function CondominioProvider({ children }: { children: ReactNode }) {
  const [residents, setResidents] = useState<Resident[]>([
    { id: "1", name: "María González", apt: "101", balance: 1500 },
    { id: "2", name: "Carlos Rodríguez", apt: "102", balance: 0 },
    { id: "3", name: "Ana Martínez", apt: "201", balance: 3200 },
    { id: "4", name: "Jorge López", apt: "202", balance: 750 },
    { id: "5", name: "Sofía Díaz", apt: "301", balance: 0 },
    { id: "6", name: "Pedro Ruiz", apt: "302", balance: 2100 },
  ]);

  const [payments, setPayments] = useState<Payment[]>([
    { id: "p1", residentId: "2", residentName: "Carlos Rodríguez", apt: "102", amount: 1500, date: "2025-01-05", method: "Tarjeta", concept: "Cuota Mensual Enero", status: "Completado" },
    { id: "p2", residentId: "5", residentName: "Sofía Díaz", apt: "301", amount: 1500, date: "2025-01-03", method: "Transferencia", concept: "Cuota Mensual Enero", status: "Completado" },
  ]);

  const [expenses, setExpenses] = useState<Expense[]>([
    { id: "e1", concept: "Luz - Áreas comunes", amount: 850, date: "2025-01-10", category: "Servicios" },
    { id: "e2", concept: "Jardinería", amount: 400, date: "2025-01-08", category: "Mantenimiento" },
    { id: "e3", concept: "Seguridad", amount: 1200, date: "2025-01-01", category: "Personal" },
  ]);

  const [maintenance, setMaintenance] = useState<Maintenance[]>([
    { id: "m1", area: "Ascensor", description: "Botón de piso 2 no funciona", status: "En Proceso", date: "2025-01-12", apt: "201" },
    { id: "m2", area: "Plomería", description: "Fuga en baño común", status: "Reportado", date: "2025-01-15", apt: "101" },
  ]);

  const addPayment = (p: Omit<Payment, "id">) => {
    setPayments((prev) => [...prev, { ...p, id: `p${Date.now()}` }]);
  };

  const addExpense = (e: Omit<Expense, "id">) => {
    setExpenses((prev) => [...prev, { ...e, id: `e${Date.now()}` }]);
  };

  const addMaintenance = (m: Omit<Maintenance, "id">) => {
    setMaintenance((prev) => [...prev, { ...m, id: `m${Date.now()}` }]);
  };

  const updateMaintenance = (id: string, status: Maintenance["status"]) => {
    setMaintenance((prev) => prev.map((m) => (m.id === id ? { ...m, status } : m)));
  };

  const payBalance = (residentId: string, amount: number, method: string) => {
    const resident = residents.find((r) => r.id === residentId);
    if (!resident) return;
    setResidents((prev) =>
      prev.map((r) => (r.id === residentId ? { ...r, balance: Math.max(0, r.balance - amount) } : r))
    );
    addPayment({
      residentId,
      residentName: resident.name,
      apt: resident.apt,
      amount,
      date: new Date().toISOString().split("T")[0],
      method,
      concept: "Pago de cuota",
      status: "Completado",
    });
  };

  return (
    <CondominioContext.Provider
      value={{ residents, payments, expenses, maintenance, addPayment, addExpense, addMaintenance, updateMaintenance, payBalance }}
    >
      {children}
    </CondominioContext.Provider>
  );
}

export function useCondominio() {
  const ctx = useContext(CondominioContext);
  if (!ctx) throw new Error("useCondominio must be used within CondominioProvider");
  return ctx;
}