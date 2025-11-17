import flet as ft
from UI.view import View
from database.meteo_dao import MeteoDao
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese = self._view.dd_mese
        if mese==None:
            self._view.create_alert("scegli un mese")
        else:
            results= MeteoDao.get_umidita_media_mese(mese)
            print(results)
            self._view.lst_result.clean()
            for result in results:
                self._view.lst_result.controls.append(ft.Text(result[0], result[1]))
            self._view.update_page()

    def handle_sequenza(self, e):
        mese = self._view.dd_mese
        if mese==None:
            self._view.create_alert("scegli un mese")

        else:
            situazioni_meta_mese= MeteoDao.get_situazione_meta_mese(mese)
            self._ricorsione([],situazioni_meta_mese)


    def _ricorsione(self,parziale, situazioni):
        #caso di uscita -> il tecnico è sistemato per i 15 giorni
        if len(parziale)==15:
            print(parziale)

        #caso ricorsione
        else:
            for situazione in situazioni: #45 oggetti situazione
                parziale.append(situazione)
                self._ricorsione(parziale,situazioni)
                parziale.pop()

    def vincoli_soddisfatti(self, parziale, situazioni):
        # se tutti i vincolo sono soddisfatti return true
        #vincolo sui tre giorni consecutivi
        if len (parziale)>0 and len(parziale)<=2:
            if situazioni.localita != parziale[0].localita:
                return False
        elif len(parziale)>2:
            sequenza_finale=parziale[-3]
            prima_fermata = sequenza_finale[0].localita
            contatore=0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    contatore+=1
                if contatore<3: #i tre elementi non sono in sequenza
                    return False
                #fare anche con il <6 giorni anche non consecutivi


        return True


    def read_mese(self, e):
        self._mese = int(e.control.value)

