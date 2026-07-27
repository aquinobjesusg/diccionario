import { BookA, Download, CheckCircle2, ArrowRight } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { Badge } from "@/app/components/ui/badge";


export function ThankYouHero() {
  return (
    <header className="relative overflow-hidden border-b border-amber-200/60 bg-gradient-to-br from-amber-100 via-honey-100 to-amber-50">
      {/* Decorative blurred orbs */}
      <div className="pointer-events-none absolute -top-24 -right-24 h-96 w-96 rounded-full bg-amber-300/30 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-32 -left-20 h-80 w-80 rounded-full bg-yellow-200/40 blur-3xl" />

      <div className="relative mx-auto max-w-5xl px-6 py-16 md:py-24 text-center">
        <Badge
          variant="outline"
          className="mb-6 border-amber-300 bg-amber-50/80 text-amber-800 backdrop-blur"
        >
          <CheckCircle2 className="mr-1.5 h-3.5 w-3.5" />
          Descarga lista
        </Badge>

        {/* Dictionary icon */}
        <div className="mx-auto mb-8 flex h-28 w-28 items-center justify-center rounded-3xl bg-gradient-to-br from-amber-500 to-yellow-600 shadow-xl shadow-amber-500/30 ring-1 ring-amber-300">
          <BookA className="h-14 w-14 text-white" strokeWidth={1.5} />
        </div>

        <h1 className="font-serif text-4xl font-bold tracking-tight text-amber-950 md:text-6xl">
          ¡Gracias por elegir <span className="text-amber-700">DiccSystemsYa</span>!
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-amber-900/70 md:text-xl">
          Tu descarga está lista. Comienza a aprender inglés de forma más
          práctica, espontánea y divertida — donde quiera que estés.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button
            size="lg"
            className="bg-amber-600 text-white shadow-lg shadow-amber-600/30 hover:bg-amber-700 hover:shadow-amber-700/40"
          >
            <Download className="mr-2 h-5 w-5" />
            Descargar para Linux (.deb)
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-amber-300 bg-white/60 text-amber-900 hover:bg-amber-50 hover:text-amber-800"
          >
            Ver otras versiones
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>

        <p className="mt-4 text-sm text-amber-800/60">
          Versión 2.4.0 · 78.4 MB · Compatible con Debian, Ubuntu, Mint
        </p>
      </div>
    </header>
  );
}