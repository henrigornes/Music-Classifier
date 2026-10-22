def Mix_harmonique(cle1, cle2):

    cle1 = str(cle1).strip().upper()
    cle2 = str(cle2).strip().upper()

    try:
        num1, lettre1 = int(cle1[:-1]), cle1[-1]
        num2, lettre2 = int(cle2[:-1]), cle2[-1]
        if num1 < 1 or num1 > 12 : 
            raise ValueError("Numéro de clé hors limites (1-12).")
        if num2 < 1 or num2 > 12 : 
            raise ValueError("Numéro de clé hors limites (1-12).")
        if lettre1 not in "AB" or lettre2 not in "AB":
            raise ValueError("Lettre de clé invalide (doit être A ou B).")
    
    except (ValueError, IndexError):
        return False

    if cle1 == cle2:
        return True
    if num1 == num2 and lettre1 != lettre2:
        return True


    if lettre1 == lettre2:
        voisin_droite = (num1 % 12) + 1
        voisin_gauche = 12 if num1 == 1 else num1 - 1

        if num2 in (voisin_droite, voisin_gauche):
            return True

    return False

def main():
    cle1 = input("Entrez la première clé (ex: 1A): ")
    cle2 = input("Entrez la deuxième clé (ex: 2B): ")

    if Mix_harmonique(cle1, cle2):
        print(f"Les clés {cle1} et {cle2} sont harmoniques.")
    else:
        print(f"Les clés {cle1} et {cle2} ne sont pas harmoniques.")

if __name__ == "__main__":
    main()
