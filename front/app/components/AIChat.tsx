import { useState, useRef, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  Sparkles, X, Send, MessageCircle, RefreshCw, Dumbbell, Gamepad2,
  BookOpen, Mic, Lightbulb, Menu, Trash2,
  Play, Square, 
} from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";

type Message = {
  role: "user" | "ai";
  content: string;
};

const quickActions = [
  { label: "Repasar", icon: RefreshCw, query: "¿Cómo funciona Repasar?" },
  { label: "Entrenamiento", icon: Dumbbell, query: "¿Cómo funciona Entrenamiento?" },
  { label: "Jugar", icon: Gamepad2, query: "¿Cómo funciona Jugar?" },
  { label: "Niveles", icon: BookOpen, query: "¿Qué niveles hay disponibles?" },
  { label: "Micrófono", icon: Mic, query: "¿Cómo uso el micrófono en Jugar?" },
];

function getAIResponse(query: string): string {
  const q = query.toLowerCase();

  if (q.includes("repasar") || q.includes("repaso")) {
    return "📚 **Repasar** te permite reforzar lo aprendido mediante tarjetas de vocabulario. Sigue estos pasos:\n\n1️⃣ Selecciona el **idioma** que quieres practicar\n2️⃣ Elige tu **nivel** (Básico, Intermedio o Avanzado)\n3️⃣ Selecciona la **modalidad** (Modismos, Palabras o Verbos Compuestos)\n4️⃣ Define la **cantidad** de palabras por página (10 a 60, o todas)\n5️⃣ Confirma y comienza a ver las tarjetas\n\nCada tarjeta muestra la palabra en inglés y su traducción al español. ¡Pulsa el ícono de audio para escuchar la pronunciación!";
  }

  if (q.includes("entrenamiento") || q.includes("entrenar")) {
    return "💪 **Entrenamiento** es práctica intensiva. Sigue los mismos 5 pasos que Repasar, pero en lugar de solo ver tarjetas, deberás **escribir la traducción** de cada palabra mostrada en inglés.\n\nAl escribir y verificar, el sistema te indicará si es correcto o no, y al final verás tus estadísticas de aciertos y errores. ¡Es ideal para dominar el vocabulario!";
  }

  if (q.includes("jugar") || q.includes("juego") || q.includes("game")) {
    return "🎮 **Jugar** es la forma más divertida de practicar. Sigue los mismos 5 pasos de configuración, pero aquí tienes **dos formas de responder**:\n\n✍️ **Escribir**: Escribe la traducción al español de la palabra mostrada\n🎤 **Hablar**: Pulsa el botón de micrófono y **pronuncia la palabra en inglés**. El sistema comparará tu pronunciación con la palabra original.\n\n¡Mezcla ambas formas para un aprendizaje completo! Recuerda permitir el acceso al micrófono cuando el navegador lo solicite.";
  }

  if (q.includes("nivel") || q.includes("niveles")) {
    return "📊 Tenemos **3 niveles** disponibles:\n\n🟢 **Básico**: Fundamentos esenciales para empezar tu camino en el idioma\n🔵 **Intermedio**: Amplía tu vocabulario y mejora tu fluidez con palabras más comunes\n🔷 **Avanzado**: Perfecciona detalles y matices del idioma con vocabulario especializado\n\nPuedes cambiar de nivel en cualquier momento configurando una nueva sesión.";
  }

  if (q.includes("modalidad") || q.includes("modalidades")) {
    return "📂 Ofrecemos **3 modalidades** de aprendizaje:\n\n💬 **Modismos**: Expresiones cotidianas y frases hechas para sonar como un nativo\n📖 **Palabras**: Vocabulario esencial organizado por temas y niveles de dificultad\n🔗 **Verbos Compuestos**: Phrasal verbs más usados con ejemplos prácticos y contextuales\n\nCada modalidad se adapta al nivel que elijas.";
  }

  if (q.includes("cantidad") || q.includes("palabras por") || q.includes("cuantas")) {
    return "🔢 Puedes elegir cuántas palabras ver por sesión:\n\n• 10 palabras\n• 20 palabras\n• 30 palabras\n• 40 palabras\n• 50 palabras\n• 60 palabras\n• Todas las palabras\n\nSi estás empezando, te recomiendo comenzar con **10-20 palabras** e ir aumentando gradualmente.";
  }

  if (q.includes("microfono") || q.includes("micrófono") || q.includes("voz") || q.includes("audio") || q.includes("pronunciacion") || q.includes("pronunciación")) {
    return "🎤 El **micrófono** está disponible en la opción **Jugar**. Aquí te explico cómo usarlo:\n\n1. Configura tu sesión en Jugar (idioma, nivel, modalidad, cantidad)\n2. Al comenzar, verás un botón circular con ícono de micrófono\n3. Púlsalo y **pronuncia en inglés** la palabra que aparece en pantalla\n4. El sistema reconocerá tu voz y la comparará con la palabra correcta\n5. Te indicará si acertaste o no\n\n💡 **Consejo**: Asegúrate de estar en un lugar sin mucho ruido y de permitir el acceso al micrófono en tu navegador.";
  }

  if (q.includes("hola") || q.includes("saludos") || q.includes("buenas") || q.includes("hey") || q.includes("hi")) {
    return "¡Hola! 👋 Soy tu asistente de **DicccSystemsYa**. Estoy aquí para ayudarte a aprovechar al máximo la plataforma.\n\nPuedes preguntarme sobre:\n• Cómo usar **Repasar**, **Entrenamiento** o **Jugar**\n• Los niveles y modalidades disponibles\n• Cómo usar el micrófono para practicar pronunciación\n• La cantidad de palabras por sesión\n\n¿Qué te gustaría saber?";
  }

  if (q.includes("ayuda") || q.includes("help") || q.includes("como") || q.includes("cómo")) {
    return "🤖 Estoy aquí para ayudarte. **DicccSystemsYa** tiene 3 opciones principales:\n\n📚 **Repasar**: Ver tarjetas de vocabulario con su traducción\n💪 **Entrenamiento**: Escribir traducciones para practicar activamente\n🎮 **Jugar**: Escribir o pronunciar palabras con el micrófono\n\nTodas siguen los mismos 5 pasos de configuración: idioma, nivel, modalidad, cantidad y confirmación. ¿Sobre cuál quieres saber más?";
  }

  if (q.includes("idioma") || q.includes("idiomas") || q.includes("ingles") || q.includes("inglés") || q.includes("español")) {
    return "🌐 Actualmente **DicccSystemsYa** soporta:\n\n🇬🇧 **Inglés**: Aprende vocabulario, modismos y verbos compuestos en inglés\n🇪🇸 **Español**: Practica tu español si es tu segundo idioma\n\nPuedes seleccionar el idioma en el primer paso de cualquier modo (Repasar, Entrenamiento o Jugar).";
  }

  if (q.includes("gracias") || q.includes("thanks")) {
    return "¡De nada! 😊 Estoy aquí para ayudarte cuando lo necesites. ¡Mucho éxito en tu aprendizaje con **DicccSystemsYa**! 🚀";
  }

  return "🤖 Entiendo tu pregunta. En **DicccSystemsYa** puedes:\n\n📚 **Repasar** vocabulario con tarjetas\n💪 **Entrenar** escribiendo traducciones\n🎮 **Jugar** escribiendo o pronunciando con micrófono\n\nCada uno sigue 5 pasos: idioma, nivel, modalidad, cantidad y confirmación. ¿Te gustaría saber más sobre alguna de estas opciones? Puedes usar los botones de acceso rápido abajo.";
}

export function AIChat() {
  // Se ejecuta una sola vez al inicializar el componente
  const delayRef = (800 * 600);
  const [isOpen, setIsOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [chatActive, setChatActive] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const startChat = () => {
    setChatActive(true);
    setMessages([
      {
        role: "ai",
        content: "¡Hola! 👋 Soy tu asistente de **DicccSystemsYa**. Estoy aquí para ayudarte a aprovechar al máximo la plataforma.\n\nPuedes preguntarme sobre cómo usar Repasar, Entrenamiento, Jugar, los niveles disponibles, el micrófono y más. ¿En qué puedo ayudarte hoy?",
      },
    ]);
    setMenuOpen(false);
  };

  const endChat = () => {
    setChatActive(false);
    setMessages([]);
    setInput("");
    setMenuOpen(false);
  };

  const handleSend = (text?: string) => {
    if (!chatActive) {
      startChat();
      return;
    }
    const message = (text || input).trim();
    if (!message) return;

    setMessages((prev) => [...prev, { role: "user", content: message }]);
    setInput("");
    setIsTyping(true);

    setTimeout(() => {
      const response = getAIResponse(message);
      setMessages((prev) => [...prev, { role: "ai", content: response }]);
      setIsTyping(false);
    }, delayRef);
  };

  const formatMessage = (content: string) => {
    return content.split("\n").map((line, i) => {
      const parts = line.split(/(\*\*[^*]+\*\*)/g);
      return (
        <p key={i} className={line.trim() === "" ? "h-2" : "mb-1"}>
          {parts.map((part, j) => {
            if (part.startsWith("**") && part.endsWith("**")) {
              return (
                <span key={j} className="font-bold text-sky-200">
                  {part.slice(2, -2)}
                </span>
              );
            }
            return <span key={j}>{part}</span>;
          })}
        </p>
      );
    });
  };

  return (
    <>
      {/* Floating button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-sky-600 to-emerald-700 text-white shadow-xl shadow-sky-900/50 transition-transform hover:scale-110"
          >
            <MessageCircle className="h-6 w-6" />
            <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold">
              1
            </span>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ x: "100%", opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: "100%", opacity: 0 }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed bottom-0 right-0 top-0 z-50 flex h-full w-full max-w-md flex-col border-l border-sky-800/60 bg-slate-900/95 shadow-2xl backdrop-blur-xl"
          >
            {/* Header */}
            <div className="relative flex items-center justify-between border-b border-sky-800/60 bg-slate-900/80 px-6 py-4">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-md">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-serif text-base font-bold text-sky-100">Asistente IA</p>
                  <p className="flex items-center gap-1 text-xs text-emerald-400">
                    <span className={`h-2 w-2 rounded-full ${chatActive ? "bg-emerald-400" : "bg-slate-500"}`} />
                    {chatActive ? "En línea" : "Desconectado"}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="flex h-9 w-9 items-center justify-center rounded-lg text-sky-300 transition-colors hover:bg-slate-800 hover:text-sky-100"
                >
                  <Menu className="h-5 w-5" />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="flex h-9 w-9 items-center justify-center rounded-lg text-sky-300 transition-colors hover:bg-slate-800 hover:text-sky-100"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              {/* Dropdown menu */}
              <AnimatePresence>
                {menuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-4 top-16 w-56 overflow-hidden rounded-xl border border-sky-800/60 bg-slate-800 shadow-2xl"
                  >
                    <div className="border-b border-sky-800/60 px-4 py-2">
                      <p className="text-xs uppercase tracking-wide text-sky-300/70">Opciones del Chat</p>
                    </div>
                    {!chatActive ? (
                      <button
                        onClick={startChat}
                        className="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-sky-100 transition-colors hover:bg-slate-700"
                      >
                        <Play className="h-4 w-4 text-emerald-400" />
                        Comenzar Chat
                      </button>
                    ) : (
                      <button
                        onClick={endChat}
                        className="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-sky-100 transition-colors hover:bg-slate-700"
                      >
                        <Square className="h-4 w-4 text-rose-400" />
                        Finalizar Chat
                      </button>
                    )}
                    <button
                      onClick={() => {
                        if (chatActive) {
                          setMessages([
                            {
                              role: "ai",
                              content: "¡Hola! 👋 Soy tu asistente de **DicccSystemsYa**. ¿En qué puedo ayudarte hoy?",
                            },
                          ]);
                        }
                        setMenuOpen(false);
                      }}
                      disabled={!chatActive}
                      className="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-sky-100 transition-colors hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-transparent"
                    >
                      <Trash2 className="h-4 w-4 text-sky-400" />
                      Limpiar Historial
                    </button>
                    <div className="border-t border-sky-800/60 px-4 py-2">
                      <p className="text-xs text-sky-300/60">DicccSystemsYa v1.0</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Messages or Welcome screen */}
            <div className="flex-1 overflow-y-auto px-4 py-6">
              {!chatActive ? (
                <div className="flex h-full flex-col items-center justify-center text-center">
                  <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-xl">
                    <Sparkles className="h-10 w-10 text-white" />
                  </div>
                  <h2 className="font-serif text-xl font-bold text-sky-100">Asistente de DicccSystemsYa</h2>
                  <p className="mt-2 max-w-xs text-sm text-sky-200/70">
                    Tu guía inteligente para aprender idiomas. Comienza a chatear para resolver tus dudas sobre Repasar, Entrenamiento y Jugar.
                  </p>
                  <Button
                    onClick={startChat}
                    className="mt-6 bg-gradient-to-r from-sky-600 to-emerald-700 text-white shadow-lg hover:from-sky-500 hover:to-emerald-600"
                  >
                    <Play className="mr-2 h-4 w-4" />
                    Comenzar Chat
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((msg, i) => (
                    <div
                      key={i}
                      className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      {msg.role === "ai" && (
                        <div className="mr-2 mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-sky-600 to-emerald-700">
                          <Sparkles className="h-4 w-4 text-white" />
                        </div>
                      )}
                      <div
                        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                          msg.role === "user"
                            ? "bg-gradient-to-br from-sky-600 to-emerald-700 text-white"
                            : "border border-sky-800/60 bg-slate-800/80 text-sky-100"
                        }`}
                      >
                        {formatMessage(msg.content)}
                      </div>
                    </div>
                  ))}

                  {isTyping && (
                    <div className="flex justify-start">
                      <div className="mr-2 mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-sky-600 to-emerald-700">
                        <Sparkles className="h-4 w-4 text-white" />
                      </div>
                      <div className="flex items-center gap-1 rounded-2xl border border-sky-800/60 bg-slate-800/80 px-4 py-4">
                        <span className="h-2 w-2 animate-bounce rounded-full bg-sky-400" style={{ animationDelay: "0ms" }} />
                        <span className="h-2 w-2 animate-bounce rounded-full bg-sky-400" style={{ animationDelay: "150ms" }} />
                        <span className="h-2 w-2 animate-bounce rounded-full bg-sky-400" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            {/* Quick actions */}
            {chatActive && messages.length <= 2 && (
              <div className="border-t border-sky-800/60 px-4 py-3">
                <p className="mb-2 flex items-center gap-1 text-xs text-sky-300/70">
                  <Lightbulb className="h-3 w-3" />
                  Preguntas frecuentes
                </p>
                <div className="flex flex-wrap gap-2">
                  {quickActions.map((action) => (
                    <button
                      key={action.label}
                      onClick={() => handleSend(action.query)}
                      className="flex items-center gap-1.5 rounded-full border border-sky-700 bg-slate-800/80 px-3 py-1.5 text-xs text-sky-200 transition-colors hover:border-sky-500 hover:bg-slate-700"
                    >
                      <action.icon className="h-3 w-3" />
                      {action.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="border-t border-sky-800/60 p-4">
              <div className="flex items-center gap-2">
                <Input
                  type="text"
                  placeholder={chatActive ? "Escribe tu pregunta..." : "Inicia el chat para escribir..."}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && input.trim()) handleSend();
                  }}
                  disabled={!chatActive}
                  className="border-sky-700 bg-slate-800 text-sky-100 placeholder:text-sky-300/40 focus:border-sky-500 disabled:opacity-40"
                />
                <Button
                  onClick={() => handleSend()}
                  disabled={!input.trim() || !chatActive}
                  size="icon"
                  className="flex-shrink-0 bg-gradient-to-br from-sky-600 to-emerald-700 text-white shadow-md hover:from-sky-500 hover:to-emerald-600 disabled:opacity-40"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}