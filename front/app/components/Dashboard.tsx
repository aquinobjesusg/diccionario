import { useState, useRef, useCallback } from "react";
import {
  BookA, LogOut, RefreshCw, Gamepad2, ArrowRight, Dumbbell, Check,
  MessageSquareQuote, BookOpen, Link2, ArrowLeft, Globe, BarChart3,
  Sparkles, Volume2, Hash, Keyboard, Send, Mic, MicOff,
  X, List,
} from "lucide-react";

import { Button } from "@/app/components/ui/button";   
import { Input } from "@/app/components/ui/input";
import { toast } from "sonner";
import { Footer } from "./Footer";
import { AIChat } from "./AIChat";

/* Tipos para Web Speech API */
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}
interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}
interface ISpeechRecognition extends EventTarget {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  start(): void;
  stop(): void;
  abort(): void;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  onstart: (() => void) | null;
}
declare global {
  interface Window {
    SpeechRecognition?: { new (): ISpeechRecognition };
    webkitSpeechRecognition?: { new (): ISpeechRecognition };
  }
}

type DashboardView =
  | "home"
  | "parametros"
  | "lista"
  | "listar-palabras"
  | "repasar"
  | "repasar-palabras"
  | "entrenamiento"
  | "entrenamiento-practicar"
  | "jugar"
  | "jugar-practicar";

const options = [
  {
    icon: List,
    title: "Ver Rango de Palabras",
    desc: "Muestra las palabras que existen y las Enumeras.",
    color: "from-sky-700 to-cyan-800",
    action: "listar-palabras" as const,
  },
  {
    icon: RefreshCw,
    title: "Repasar",
    desc: "Refuerza lo aprendido con repaso espaciado y ejercicios interactivos.",
    color: "from-sky-700 to-cyan-800",
    action: "repasar-palabras" as const,
  },
  {
    icon: Dumbbell,
    title: "Entrenamiento",
    desc: "Practica intensivamente para dominar el idioma con rutinas guiadas.",
    color: "from-emerald-700 to-teal-800",
    action: "entrenamiento-practicar" as const,
  },
  {
    icon: Gamepad2,
    title: "Jugar",
    desc: "Pon a prueba tu vocabulario escribiendo o pronunciando las palabras.",
    color: "from-teal-700 to-sky-800",
    action: "jugar-practicar" as const,
  },
];

const idiomas = [
  { id: "es", label: "Español", flag: "🇪🇸" },
  { id: "en", label: "Inglés", flag: "🇬🇧" },
];

const niveles = [
  { id: "basico", label: "Básico", desc: "Fundamentos esenciales para empezar.", color: "from-emerald-600 to-teal-700" },
  { id: "intermedio", label: "Intermedio", desc: "Amplía vocabulario y mejora fluidez.", color: "from-sky-600 to-cyan-700" },
  { id: "avanzado", label: "Avanzado", desc: "Perfecciona detalles y matices del idioma.", color: "from-teal-600 to-sky-700" },
];

const modalidades = [
  { id: "modismos", icon: MessageSquareQuote, title: "Modismos", desc: "Expresiones cotidianas y frases hechas para sonar como un nativo.", color: "from-sky-600 to-cyan-700" },
  { id: "palabras", icon: BookOpen, title: "Palabras", desc: "Vocabulario esencial organizado por temas y niveles de dificultad.", color: "from-emerald-600 to-teal-700" },
  { id: "verbos", icon: Link2, title: "Verbos Compuestos", desc: "Phrasal verbs más usados con ejemplos prácticos y contextuales.", color: "from-teal-600 to-sky-700" },
];

const cantidades = [
  { id: "10", label: "10 palabras" },
  { id: "20", label: "20 palabras" },
  { id: "30", label: "30 palabras" },
  { id: "40", label: "40 palabras" },
  { id: "50", label: "50 palabras" },
  { id: "60", label: "60 palabras" },
  { id: "todas", label: "Todas las palabras" },
];

const palabrasLista = [
  { en: "House", es: "Casa" },
  { en: "Dog", es: "Perro" },
  { en: "Cat", es: "Gato" },
  { en: "Book", es: "Libro" },
  { en: "Water", es: "Agua" },
  { en: "Friend", es: "Amigo" },
  { en: "City", es: "Ciudad" },
  { en: "Food", es: "Comida" },
  { en: "Car", es: "Carro" },
  { en: "Day", es: "Día" },
  { en: "Night", es: "Noche" },
  { en: "Sun", es: "Sol" },
  { en: "Moon", es: "Luna" },
  { en: "Sky", es: "Cielo" },
  { en: "Tree", es: "Árbol" },
  { en: "Road", es: "Camino" },
  { en: "Door", es: "Puerta" },
  { en: "Window", es: "Ventana" },
  { en: "Table", es: "Mesa" },
  { en: "Chair", es: "Silla" },
];

const steps = [
  { num: 1, label: "Idioma" },
  { num: 2, label: "Nivel" },
  { num: 3, label: "Modalidad" },
  { num: 4, label: "Cantidad" },
  { num: 5, label: "Confirmar" },
];




export function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [view, setView] = useState<DashboardView>("home");
  const [step, setStep] = useState(1);
  const [idioma, setIdioma] = useState<string | null>(null);
  const [nivel, setNivel] = useState<string | null>(null);
  const [modalidad, setModalidad] = useState<string | null>(null);
  const [cantidad, setCantidad] = useState<string | null>(null);

  // Práctica state (entrenamiento & jugar)
  const [palabraIndex, setPalabraIndex] = useState(0);
  const [respuesta, setRespuesta] = useState("");
  const [resultados, setResultados] = useState<{ correcta: boolean; palabra: string; respuesta: string }[]>([]);
  const [mostrarResultado, setMostrarResultado] = useState(false);
  const [ultimaRespuesta, setUltimaRespuesta] = useState("");

  // Micrófono state
  const [escuchando, setEscuchando] = useState(false);
  const [soportaVoz, setSoportaVoz] = useState(true);
  const recognitionRef = useRef<ISpeechRecognition | null>(null);
/*
  const handleOptionClick = (action:  "parametros" | "repasar" |  "lista" | "entrenamiento" | "jugar" | null) => {
    if (action) {
      setView(action);
      setStep(1);
      setIdioma(null);
      setNivel(null);
      setModalidad(null);
      setCantidad(null);
      setPalabraIndex(0);
      setResultados([]);
      setRespuesta("");
      setMostrarResultado(false);
    } else {
      toast.info("Próximamente disponible");
    }
  };
*/
const handleOptionClick = (action: DashboardView) => {
  setView(action);
  setStep(1);
  setIdioma(null);
  setNivel(null);
  setModalidad(null);
  setCantidad(null);
  setPalabraIndex(0);
  setResultados([]);
  setRespuesta("");
  setMostrarResultado(false);
};

  const handleContinue = () => {
    if (step < 5) {
      setStep(step + 1);
    } else {
      if (view === "lista") {
        setView("listar-palabras");

      } else if (view === "repasar") {
          setView("repasar-palabras");

      } else if (view === "entrenamiento") {
        setView("entrenamiento-practicar");

      } else if (view === "jugar") {
        setView("jugar-practicar");

      } else if (view === "parametros") {
        setView("parametros");
      }
      setPalabraIndex(0);
      setResultados([]);
      setRespuesta("");
      setMostrarResultado(false);
      toast.success("¡Listo! Comencemos.");
    }
  };

  const canContinue = () => {
    if (step === 1) return idioma !== null;
    if (step === 2) return nivel !== null;
    if (step === 3) return modalidad !== null;
    if (step === 4) return cantidad !== null;
    if (step === 5) return true;
    return false;
  };

  const getPalabras = () => {
    if (cantidad === "todas") return palabrasLista;
    const n = parseInt(cantidad || "10", 10);
    return palabrasLista.slice(0, n);
  };

  const verificarRespuesta = (resp: string) => {
    const palabraActual = getPalabras()[palabraIndex];
    const esCorrecta = resp.trim().toLowerCase() === palabraActual.es.toLowerCase();
    setResultados([...resultados, { correcta: esCorrecta, palabra: palabraActual.en, respuesta: resp }]);
    setUltimaRespuesta(resp);
    setMostrarResultado(true);
  };

  const verificarPronunciacion = (reconocido: string) => {
    const palabraActual = getPalabras()[palabraIndex];
    const esCorrecta = reconocido.trim().toLowerCase() === palabraActual.en.toLowerCase();
    setResultados([...resultados, { correcta: esCorrecta, palabra: palabraActual.en, respuesta: reconocido }]);
    setUltimaRespuesta(reconocido);
    setMostrarResultado(true);
  };

  const siguientePalabra = () => {
    if (palabraIndex < getPalabras().length - 1) {
      setPalabraIndex(palabraIndex + 1);
      setRespuesta("");
      setMostrarResultado(false);
      setUltimaRespuesta("");
    } else {
      const correctas = resultados.filter((r) => r.correcta).length;
      const total = getPalabras().length;
      setView("home");
      toast.success(`¡Completado! Aciertos: ${correctas}/${total}`);
    }
  };

  const iniciarMicrofono = useCallback(() => {
    const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionClass) {
      setSoportaVoz(false);
      toast.error("Tu navegador no soporta reconocimiento de voz");
      return;
    }

    if (escuchando) {
      recognitionRef.current?.stop();
      setEscuchando(false);
      return;
    }

    const recognition = new SpeechRecognitionClass();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setEscuchando(true);
    };

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      verificarPronunciacion(transcript);
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      setEscuchando(false);
      toast.error("No se pudo capturar el audio. Intenta de nuevo.");
    };

    recognition.onend = () => {
      setEscuchando(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  }, [escuchando, palabraIndex]);

  const renderStepContent = () => {
    if (step === 1) {
      return (
        <div className="animate-in fade-in duration-300">
          <h2 className="mb-6 font-serif text-xl font-bold text-sky-100">1. Selecciona el Idioma</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {idiomas.map((opt) => (
              <button
                key={opt.id}
                onClick={() => setIdioma(opt.id)}
                className={`flex items-center gap-4 rounded-2xl border p-6 text-left transition-all ${
                  idioma === opt.id ? "border-sky-400 bg-slate-800 ring-2 ring-sky-500" : "border-sky-800/70 bg-slate-900/90 hover:border-sky-600 hover:bg-slate-800"
                }`}
              >
                <span className="text-4xl">{opt.flag}</span>
                <div>
                  <p className="font-serif text-lg font-bold text-sky-100">{opt.label}</p>
                  <p className="text-sm text-sky-200/70">Aprende {opt.label}</p>
                </div>
                {idioma === opt.id && <Check className="ml-auto h-5 w-5 text-sky-400" />}
              </button>
            ))}
          </div>
        </div>
      );
    }
    if (step === 2) {
      return (
        <div className="animate-in fade-in duration-300">
          <h2 className="mb-6 font-serif text-xl font-bold text-sky-100">2. Selecciona el Nivel de Repaso</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {niveles.map((opt) => (
              <button
                key={opt.id}
                onClick={() => setNivel(opt.id)}
                className={`relative overflow-hidden rounded-2xl border p-6 text-left transition-all ${
                  nivel === opt.id ? "border-sky-400 bg-slate-800 ring-2 ring-sky-500" : "border-sky-800/70 bg-slate-900/90 hover:border-sky-600 hover:bg-slate-800"
                }`}
              >
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${opt.color} shadow-lg`}>
                  <BarChart3 className="h-6 w-6 text-white" strokeWidth={1.8} />
                </div>
                <h3 className="font-serif text-lg font-bold text-sky-100">{opt.label}</h3>
                <p className="mt-1 text-sm text-sky-200/70">{opt.desc}</p>
                {nivel === opt.id && (
                  <div className="absolute right-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-sky-500 text-white">
                    <Check className="h-4 w-4" />
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      );
    }
    if (step === 3) {
      return (
        <div className="animate-in fade-in duration-300">
          <h2 className="mb-6 font-serif text-xl font-bold text-sky-100">3. Selecciona la Modalidad</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {modalidades.map((opt) => (
              <button
                key={opt.id}
                onClick={() => setModalidad(opt.id)}
                className={`relative overflow-hidden rounded-2xl border p-6 text-left transition-all ${
                  modalidad === opt.id ? "border-sky-400 bg-slate-800 ring-2 ring-sky-500" : "border-sky-800/70 bg-slate-900/90 hover:border-sky-600 hover:bg-slate-800"
                }`}
              >
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${opt.color} shadow-lg`}>
                  <opt.icon className="h-6 w-6 text-white" strokeWidth={1.8} />
                </div>
                <h3 className="font-serif text-lg font-bold text-sky-100">{opt.title}</h3>
                <p className="mt-1 text-sm text-sky-200/70">{opt.desc}</p>
                {modalidad === opt.id && (
                  <div className="absolute right-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-sky-500 text-white">
                    <Check className="h-4 w-4" />
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      );
    }
    if (step === 4) {
      return (
        <div className="animate-in fade-in duration-300">
          <h2 className="mb-6 font-serif text-xl font-bold text-sky-100">4. Selecciona la cantidad de palabras a mostrar por página</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {cantidades.map((opt) => (
              <button
                key={opt.id}
                onClick={() => setCantidad(opt.id)}
                className={`flex items-center gap-4 rounded-2xl border p-5 text-left transition-all ${
                  cantidad === opt.id ? "border-sky-400 bg-slate-800 ring-2 ring-sky-500" : "border-sky-800/70 bg-slate-900/90 hover:border-sky-600 hover:bg-slate-800"
                }`}
              >
                <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${cantidad === opt.id ? "bg-sky-600" : "bg-sky-800/50"}`}>
                  <Hash className="h-5 w-5 text-white" />
                </div>
                <span className="font-serif text-base font-bold text-sky-100">{opt.label}</span>
                {cantidad === opt.id && <Check className="ml-auto h-5 w-5 text-sky-400" />}
              </button>
            ))}
          </div>
        </div>
      );
    }
    if (step === 5) {
      return (
        <div className="animate-in fade-in duration-300">
          <h2 className="mb-6 font-serif text-xl font-bold text-sky-100">5. Listo para Continuar</h2>
          <div className="rounded-2xl border border-sky-800/70 bg-slate-900/90 p-8 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-lg">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="font-serif text-xl font-bold text-sky-100">Resumen de tu sesión</h3>
                <p className="text-sm text-sky-200/70">Revisa que todo esté correcto antes de comenzar.</p>
              </div>
            </div>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Idioma</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">
                  {idiomas.find((i) => i.id === idioma)?.flag} {idiomas.find((i) => i.id === idioma)?.label}
                </p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Nivel</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{niveles.find((n) => n.id === nivel)?.label}</p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Modalidad</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{modalidades.find((m) => m.id === modalidad)?.title}</p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Cantidad</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{cantidades.find((c) => c.id === cantidad)?.label}</p>
              </div>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  const renderPractica = (modo: "entrenamiento" | "jugar") => {
    const palabras = getPalabras();
    const palabraActual = palabras[palabraIndex];
    const ultimoResultado = resultados[resultados.length - 1];

    return (
      <>

        <button
          onClick={() => setView("home")}
          className="mb-6 flex items-center gap-1 text-sm text-sky-300 transition-colors hover:text-sky-100"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver a Inicio
        </button>

        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {modo === "entrenamiento" ? <Keyboard className="h-6 w-6 text-sky-300" /> : <Gamepad2 className="h-6 w-6 text-sky-300" />}
            <h1 className="font-serif text-2xl font-bold text-sky-100 md:text-3xl">
              {modo === "entrenamiento" ? "Práctica de Traducción" : "Juego de Traducción"}
            </h1>
          </div>
          <div className="rounded-lg border border-sky-800/70 bg-slate-900/90 px-4 py-2 text-sm text-sky-200">
            Palabra {palabraIndex + 1} de {palabras.length}
          </div>
        </div>

        {/* Progress bar */}
        <div className="mb-8 h-2 w-full overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full rounded-full bg-gradient-to-r from-sky-500 to-emerald-500 transition-all duration-300"
            style={{ width: `${((palabraIndex + (mostrarResultado ? 1 : 0)) / palabras.length) * 100}%` }}
          />
        </div>

        <div className="mx-auto max-w-2xl">
          <div className="rounded-2xl border border-sky-800/70 bg-slate-900/90 p-8 shadow-lg">
            <p className="text-center text-sm uppercase tracking-wide text-sky-300/70">
              {modo === "jugar" ? "Traduce al español o pronuncia en inglés" : "Traduce al español"}
            </p>
            <p className="mt-4 text-center font-serif text-5xl font-bold text-sky-100">{palabraActual.en}</p>

            <div className="mt-8">
              <Input
                type="text"
                placeholder="Escribe la traducción aquí..."
                value={respuesta}
                onChange={(e) => setRespuesta(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !mostrarResultado && respuesta.trim()) verificarRespuesta(respuesta);
                  else if (e.key === "Enter" && mostrarResultado) siguientePalabra();
                }}
                disabled={mostrarResultado}
                className="h-14 border-sky-700 bg-slate-800 text-center text-lg text-sky-100 placeholder:text-sky-300/40 focus:border-sky-500"
              />
            </div>

            {/* Microphone button - only in jugar mode */}
            {modo === "jugar" && (
              <div className="mt-6 flex flex-col items-center gap-3">
                <div className="flex items-center gap-4">
                  <div className="h-px w-16 bg-sky-800/60" />
                  <span className="text-xs uppercase tracking-wide text-sky-300/60">o</span>
                  <div className="h-px w-16 bg-sky-800/60" />
                </div>
                <button
                  onClick={iniciarMicrofono}
                  disabled={mostrarResultado || !soportaVoz}
                  className={`flex h-20 w-20 items-center justify-center rounded-full transition-all ${
                    escuchando
                      ? "animate-pulse bg-rose-600 shadow-lg shadow-rose-900/50"
                      : "bg-gradient-to-br from-sky-600 to-emerald-700 shadow-lg hover:from-sky-500 hover:to-emerald-600"
                  } disabled:opacity-40 disabled:hover:from-sky-600 disabled:hover:to-emerald-700`}
                >
                  {escuchando ? <MicOff className="h-8 w-8 text-white" /> : <Mic className="h-8 w-8 text-white" />}
                </button>
                <p className="text-sm text-sky-200/70">
                  {escuchando ? "Escuchando... Di la palabra en inglés" : "Pulsa el micrófono y pronuncia la palabra"}
                </p>
              </div>
            )}

            {mostrarResultado && (
              <div className={`mt-6 rounded-xl border p-4 ${ultimoResultado?.correcta ? "border-emerald-600 bg-emerald-900/30" : "border-rose-600 bg-rose-900/30"}`}>
                <div className="flex items-center gap-3">
                  {ultimoResultado?.correcta ? (
                    <Check className="h-6 w-6 text-emerald-400" />
                  ) : (
                    <X className="h-6 w-6 text-rose-400" />
                  )}
                  <div>
                    {ultimoResultado?.correcta ? (
                      <p className="font-bold text-emerald-300">¡Correcto!</p>
                    ) : (
                      <>
                        <p className="font-bold text-rose-300">Incorrecto.</p>
                        <p className="text-sm text-rose-200/80">
                          Tu respuesta: <span className="font-bold">{ultimaRespuesta}</span>
                        </p>
                        <p className="text-sm text-rose-200/80">
                          La respuesta correcta es: <span className="font-bold">{palabraActual.es}</span>
                        </p>
                      </>
                    )}
                  </div>
                </div>
              </div>
            )}

            <div className="mt-6 flex justify-center">
              {!mostrarResultado ? (
                <Button
                  onClick={() => verificarRespuesta(respuesta)}
                  disabled={!respuesta.trim()}
                  className="bg-gradient-to-r from-sky-600 to-emerald-700 text-white shadow-lg hover:from-sky-500 hover:to-emerald-600 disabled:opacity-40"
                >
                  <Send className="mr-2 h-4 w-4" />
                  Verificar
                </Button>
              ) : (
                <Button
                  onClick={siguientePalabra}
                  className="bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg hover:from-emerald-500 hover:to-teal-600"
                >
                  {palabraIndex < palabras.length - 1 ? "Siguiente" : "Finalizar"}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              )}
            </div>
          </div>

          {/* Stats */}
          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="rounded-xl border border-sky-800/70 bg-slate-900/90 p-4 text-center">
              <p className="text-xs uppercase tracking-wide text-sky-300/70">Aciertos</p>
              <p className="mt-1 font-serif text-2xl font-bold text-emerald-300">{resultados.filter((r) => r.correcta).length}</p>
            </div>
            <div className="rounded-xl border border-sky-800/70 bg-slate-900/90 p-4 text-center">
              <p className="text-xs uppercase tracking-wide text-sky-300/70">Errores</p>
              <p className="mt-1 font-serif text-2xl font-bold text-rose-300">{resultados.filter((r) => !r.correcta).length}</p>
            </div>
            <div className="rounded-xl border border-sky-800/70 bg-slate-900/90 p-4 text-center">
              <p className="text-xs uppercase tracking-wide text-sky-300/70">Restantes</p>
              <p className="mt-1 font-serif text-2xl font-bold text-sky-100">{palabras.length - resultados.length}</p>
            </div>
          </div>
        </div>
      </>
    );
  };

  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-b from-sky-900 via-cyan-900 to-slate-900">
      {/* Top bar */}
      <div className="border-b border-sky-800/60 bg-slate-900/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-md">
              <BookA className="h-5 w-5 text-white" strokeWidth={1.8} />
            </div>
            <div>
              <p className="font-serif text-lg font-bold text-sky-100">DicccSystemsYa</p>
              <p className="text-xs text-sky-200/80">Panel de Administración</p>
            </div>
          </div>
          <Button
            variant="outline"
            onClick={onLogout}
            className="border-sky-700 bg-slate-900/60 text-sky-100 hover:bg-slate-800 hover:text-white"
          >
            <LogOut className="mr-2 h-4 w-4" />
            Cerrar Sesión
          </Button>
        </div>
      </div>

      



      


      {/* Main content */}
      <div className="flex-1 mx-auto w-full max-w-6xl px-6 py-12 md:py-16">

        <div className="animate-in fade-in duration-300">
          <div className="rounded-2xl border border-sky-800/70 bg-slate-900/90 p-8 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-lg">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="font-serif text-xl font-bold text-sky-100">Datos de tu sesión</h3>
                            <div className="mt-10 flex justify-center">
            </div>

              </div>
            </div>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Idioma</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">
                  {idiomas.find((i) => i.id === idioma)?.flag} {idiomas.find((i) => i.id === idioma)?.label}
                </p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Nivel</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{niveles.find((n) => n.id === nivel)?.label}</p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Modalidad</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{modalidades.find((m) => m.id === modalidad)?.title}</p>
              </div>
              <div className="rounded-xl border border-sky-800/60 bg-slate-800/50 p-4">
                <p className="text-xs uppercase tracking-wide text-sky-300/70">Rango</p>
                <p className="mt-1 font-serif text-lg font-bold text-sky-100">{cantidades.find((c) => c.id === cantidad)?.label}</p>
              </div>
            </div>
            <br></br>

            <br></br>
                          <Button
                onClick={() => {
                  setView("parametros");
                  toast.success("¡Valores Asignados!");
                }}
                className="bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg hover:from-emerald-500 hover:to-teal-600"
              >
                Asignar Valores de la Sesión
              </Button>

          </div>
        </div>

        <br></br>

        {view === "home" && (
          <>
            <div className="mb-10">
              <h1 className="font-serif text-3xl font-bold text-sky-100 md:text-4xl">Bienvenido de nuevo, Jesús</h1>
              <p className="mt-2 text-sky-200/80">¿Qué te gustaría hacer hoy para mejorar tu inglés?</p>
            </div>
            <div className="grid gap-6 md:grid-cols-3">
              {options.map((opt) => (

                <button
                  key={opt.title}
                  onClick={() => handleOptionClick(opt.action)}
                  className="group relative overflow-hidden rounded-2xl border border-sky-800/70 bg-slate-900/90 p-8 text-left shadow-sm backdrop-blur transition-all hover:-translate-y-1 hover:border-sky-600 hover:bg-slate-800 hover:shadow-xl hover:shadow-sky-900/50"
                >
                  <div className={`mb-6 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${opt.color} shadow-lg`}>
                    <opt.icon className="h-8 w-8 text-white" strokeWidth={1.8} />
                  </div>
                  <h3 className="font-serif text-xl font-bold text-sky-100">{opt.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-sky-200/80">{opt.desc}</p>
                  <div className="mt-6 flex items-center gap-1 text-sm font-medium text-sky-300 opacity-0 transition-opacity group-hover:opacity-100">
                    Comenzar
                    <ArrowRight className="h-4 w-4" />
                  </div>
                </button>
              ))}

            </div>
          </>
        )}


        {(view === "parametros" ) && (
          <>
            <button
              onClick={() => setView("home")}
              className="mb-6 flex items-center gap-1 text-sm text-sky-300 transition-colors hover:text-sky-100"
            >
              <ArrowLeft className="h-4 w-4" />
              Volver al inicio
            </button>

            <div className="mb-10">
              <h1 className="font-serif text-3xl font-bold text-sky-100 md:text-4xl">
                Asignar Valores
              </h1>
              <p className="mt-2 text-sky-200/80">Sigue los pasos para configurar tu sesión.</p>
            </div>

            {/* Step indicator */}
            <div className="mb-12 flex items-center justify-between">
              {steps.map((s, i) => (
                <div key={s.num} className="flex flex-1 items-center">
                  <div className="flex flex-col items-center gap-2">
                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold transition-all ${
                        step >= s.num ? "bg-sky-600 text-white shadow-lg shadow-sky-900/50" : "border border-sky-700 bg-slate-800 text-sky-300"
                      }`}
                    >
                      {step > s.num ? <Check className="h-5 w-5" /> : s.num}
                    </div>
                    <span className={`text-xs font-medium ${step >= s.num ? "text-sky-100" : "text-sky-300/60"}`}>{s.label}</span>
                  </div>
                  {i < steps.length - 1 && (
                    <div className={`mx-2 h-0.5 flex-1 rounded-full transition-colors ${step > s.num ? "bg-sky-600" : "bg-sky-800/60"}`} />
                  )}
                </div>
              ))}
            </div>

            {renderStepContent()}

            {/* Navigation */}
            <div className="mt-10 flex items-center justify-between">
              <Button
                variant="outline"
                onClick={() => (step > 1 ? setStep(step - 1) : setView("home"))}
                className="border-sky-700 bg-transparent text-sky-100 hover:bg-slate-800 hover:text-white"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                {step > 1 ? "Atrás" : "Cancelar"}
              </Button>
              {step === 5 && (
                  <Button
                    onClick={() => (setView("home"))}
                    disabled={!canContinue()}
                    className="bg-gradient-to-r from-sky-600 to-emerald-700 text-white shadow-lg hover:from-sky-500 hover:to-emerald-600 disabled:opacity-40"
                  >
                    {step === 5 ? "Comenzar" : "Continuar"}
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
              )
              } 
              { step !== 5 && (
              <Button
                onClick={handleContinue}
                disabled={!canContinue()}
                className="bg-gradient-to-r from-sky-600 to-emerald-700 text-white shadow-lg hover:from-sky-500 hover:to-emerald-600 disabled:opacity-40"
              >
                {step === 5 ? "Comenzar" : "Continuar"}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              )
               } 
            </div>
          </>
        )}


        {view === "repasar-palabras" && (
          <>
            <button
              onClick={() => setView("home")}
              className="mb-6 flex items-center gap-1 text-sm text-sky-300 transition-colors hover:text-sky-100"
            >
              <ArrowLeft className="h-4 w-4" />
              Volver a Inicio
            </button>

            <div className="mb-8 flex items-center gap-3">
              <Globe className="h-6 w-6 text-sky-300" />
              <h1 className="font-serif text-2xl font-bold text-sky-100 md:text-3xl">
                Repaso: {modalidades.find((m) => m.id === modalidad)?.title} ({niveles.find((n) => n.id === nivel)?.label})
              </h1>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {getPalabras().map((palabra, i) => (
                <div
                  key={i}
                  className="group rounded-2xl border border-sky-800/70 bg-slate-900/90 p-6 shadow-sm backdrop-blur transition-all hover:border-sky-600 hover:bg-slate-800 hover:shadow-lg"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-wide text-sky-300/70">Inglés</p>
                      <p className="mt-1 font-serif text-2xl font-bold text-sky-100">{palabra.en}</p>
                    </div>
                    <button
                      onClick={() => toast.info(`Reproduciendo: ${palabra.en}`)}
                      className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-800/50 text-sky-300 transition-colors hover:bg-sky-700 hover:text-white"
                    >
                      <Volume2 className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="my-4 h-px bg-sky-800/60" />
                  <div>
                    <p className="text-xs uppercase tracking-wide text-sky-300/70">Español</p>
                    <p className="mt-1 font-serif text-xl font-bold text-emerald-300">{palabra.es}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-10 flex justify-center">
              <Button
                onClick={() => {
                  setView("home");
                  toast.success("¡Repaso completado!");
                }}
                className="bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg hover:from-emerald-500 hover:to-teal-600"
              >
                <Check className="mr-2 h-4 w-4" />
                Finalizar Repaso
              </Button>
            </div>
          </>
        )}

        {view === "listar-palabras" && (
          <>
            <button
              onClick={() => setView("home")}
              className="mb-6 flex items-center gap-1 text-sm text-sky-300 transition-colors hover:text-sky-100"
            >
              <ArrowLeft className="h-4 w-4" />
              Volver a Inicio
            </button>

            <div className="mb-8 flex items-center gap-3">
              <Globe className="h-6 w-6 text-sky-300" />
              <h1 className="font-serif text-2xl font-bold text-sky-100 md:text-3xl">
                Cantidad de Palabras en la Lista: {getPalabras().length}
              </h1>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {getPalabras().map((palabra, i) => (
                <div
                  key={i}
                  className="group rounded-2xl border border-sky-800/70 bg-slate-900/90 p-6 shadow-sm backdrop-blur transition-all hover:border-sky-600 hover:bg-slate-800 hover:shadow-lg"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-wide text-sky-300/70">Inglés</p>
                      <p className="mt-1 font-serif text-2xl font-bold text-sky-100">{palabra.en}</p>
                    </div>
                    <button
                      className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-800/50 text-sky-300 transition-colors hover:bg-sky-700 hover:text-white"
                    >
                      <p className="mt-1 font-serif text-2xl font-bold text-sky-100">{i+1}</p>
                    </button>
                  </div>
                  <div className="my-4 h-px bg-sky-800/60" />
                  <div>
                    <p className="text-xs uppercase tracking-wide text-sky-300/70">Español</p>
                    <p className="mt-1 font-serif text-xl font-bold text-emerald-300">{palabra.es}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-10 flex justify-center">
              <Button
                onClick={() => {
                  setView("home");
                  toast.success("¡Repaso completado!");
                }}
                className="bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg hover:from-emerald-500 hover:to-teal-600"
              >
                <Check className="mr-2 h-4 w-4" />
                Regresar
              </Button>
            </div>
          </>
        )}

        {view === "entrenamiento-practicar" && renderPractica("entrenamiento")}

        {view === "jugar-practicar" && renderPractica("jugar")}

      </div>

      <Footer />
      <AIChat />
    </div>
  );
}