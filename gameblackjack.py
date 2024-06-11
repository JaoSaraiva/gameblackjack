import random
#GAME TRADICIONAL DE CARTAS - BLACKJACK

class Carta:
    def __init__(self, naipe, classe):
        self.naipe = naipe
        self.classe = classe
    def __str__(self):
        return f"{self.classe['classe']} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []
        naipes = ["espadas", "paus", "copas", "ouros"]
        classes = [
                {"classe": "A", "valor": 11},
                {"classe": "2", "valor": 2},
                {"classe": "3", "valor": 3},
                {"classe": "4", "valor": 4},
                {"classe": "5", "valor": 5},
                {"classe": "6", "valor": 6},
                {"classe": "7", "valor": 7},
                {"classe": "8", "valor": 8},
                {"classe": "9", "valor": 9},
                {"classe": "10", "valor": 10},
                {"classe": "J", "valor": 10},
                {"classe": "Q", "valor": 10},
                {"classe": "K", "valor": 10},
            ]
        for naipe in naipes:
            for classe in classes:
                self.cartas.append(Carta(naipe, classe))
        
    def shuffle(self):
        if len(self.cartas) > 1:
            random.shuffle(self.cartas)
    
    def distribuir(self, numero):
        distribuicao_cartas = []
        for x in range(numero):
            if len(self.cartas) > 0:
                carta = self.cartas.pop()
                distribuicao_cartas.append(carta)
        return distribuicao_cartas

class Mao:
    def __init__(self, distribuicao=False):
        self.cartas = []
        self.valor = 0
        self.distribuicao = distribuicao

    def add_carta(self, lista_de_carta):
        self.cartas.extend(lista_de_carta)

    def calcular_valor(self):
        self.valor = 0
        tem_as = False

        for carta in self.cartas:
            valor_da_carta = int(carta.classe["valor"])
            self.valor += valor_da_carta
            if carta.classe["classe"] == "A":
                tem_as = True

        if tem_as and self.valor > 21:
            self.valor -= 10

    def obter_valor(self):
        self.calcular_valor()
        return self.valor

    def blackjack(self):
        return self.obter_valor() == 21

    def mostrar(self, mostrar_toda_distribuicao_carta=False):
        print(f'''{"Mão do distribuidor" if self.distribuicao else "Sua mão"}:''')
        for indice, carta in enumerate(self.cartas):
            if indice == 0 and self.distribuicao \
            and not mostrar_toda_distribuicao_carta and not self.blackjack():
                print("carta oculta")
            else:
                print(carta)

        if not self.distribuicao:
            print("Valor:", self.obter_valor())
        print()

class Jogo:
    def jogar(self):
        numero_jogo = 0
        jogos_para_jogar = 0

        while jogos_para_jogar <= 0:
            try:
                jogos_para_jogar = int(input("Quantos jogos você quer jogar?"))
            except:
                print("Você deve inserir um número.")

        while numero_jogo < jogos_para_jogar:
            numero_jogo += 1

            baralho = Baralho()
            baralho.shuffle()

            mao_do_jogador = Mao()
            mao_do_distribuidor = Mao(distribuicao=True)

            for i in range(2):
                mao_do_jogador.add_carta(baralho.distribuir(1))
                mao_do_distribuidor.add_carta(baralho.distribuir(1))

            print()
            print("*" * 30)
            print(f"Jogo {numero_jogo} de {jogos_para_jogar}")
            print("*" * 30)
            mao_do_jogador.mostrar()
            mao_do_distribuidor.mostrar()

            if self.verificar_vencedor(mao_do_jogador, mao_do_distribuidor):
                continue

            escolha = ""
            while mao_do_jogador.obter_valor() < 21 and escolha not in ["f", "ficar"]:
                escolha = input("Por favor, escolha bater ou ficar: ").lower()
                print()
                while escolha not in ["b", "f", "bater", "ficar"]:
                    escolha = input("Por favor, digite bater ou ficar (ou B/F) ").lower()
                    print()
                if escolha in ["bater", "b"]:
                    mao_do_jogador.add_carta(baralho.distribuir(1))
                    mao_do_jogador.mostrar()
                    
            if self.verificar_vencedor(mao_do_jogador, mao_do_distribuidor):
                continue

            valor_da_mao_do_jogador = mao_do_jogador.obter_valor()
            valor_da_mao_do_distribuidor = mao_do_distribuidor.obter_valor()

            while valor_da_mao_do_distribuidor < 17:
                mao_do_distribuidor.add_carta(baralho.distribuir(1))
                valor_da_mao_do_distribuidor = mao_do_distribuidor.obter_valor()

            mao_do_distribuidor.mostrar(mostrar_toda_distribuicao_carta=True)

            if self.verificar_vencedor(mao_do_jogador, mao_do_distribuidor):
                continue

            print("Resultado Final")
            print("Suas mãos:", valor_da_mao_do_jogador)
            print("Mãos do distribuidor:", valor_da_mao_do_distribuidor)

            self.verificar_vencedor(mao_do_jogador, mao_do_distribuidor, True)

        print("\nOBG por jogar!")

    def verificar_vencedor(self, mao_do_jogador, mao_do_distribuidor, fim_de_jogo=False):
        if not fim_de_jogo:
            if mao_do_jogador.obter_valor() > 21:
                print("Você fracassou. Vitória do distribuidor! 😭")
                return True
            elif mao_do_distribuidor.obter_valor() > 21:
                print("Distribuidor preso. Você ganha! 😀")
                return True
            elif mao_do_distribuidor.blackjack() and mao_do_jogador.blackjack():
                print("Ambos os jogadores têm blackjack! Gravata! 😑")
                return True
            elif mao_do_jogador.blackjack():
                print("Você tem blackjack. Você ganha! 😀")
                return True
            elif mao_do_distribuidor.blackjack():
                print("O distribuidor tem blackjack. Vitória do distribuidor! 😭")
                return True
        else:
            if mao_do_jogador.obter_valor() > mao_do_distribuidor.obter_valor():
                print("Você ganha! 😀")
            elif mao_do_jogador.obter_valor() == mao_do_distribuidor.obter_valor():
                print("Gravata! 😑")
            else:
                print("Vitória do distribuidor. 😭")
            return True
        return False

g = Jogo()
g.jogar()
