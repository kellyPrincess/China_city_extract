

if __name__ == '__main__':

    file = ["name_{}".format(i) for i in range(14)]
    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14 = [open(i, "w", encoding="utf-8") for i in file]

    cnt = 0
    with open("ent_01", "r", encoding="utf-8") as f:
        for line in f:
            cnt += 1
            if cnt <= (200 * 10000):
                f1.write(line.strip() + "\n")
            elif (200 * 10000) < cnt <= (400 * 10000):
                f2.write(line.strip() + "\n")
            elif (400 * 10000) < cnt <= (600 * 10000):
                f3.write(line.strip() + "\n")
            elif (600 * 10000) < cnt <= (800 * 10000):
                f4.write(line.strip() + "\n")
            elif (800 * 10000) < cnt <= (1000 * 10000):
                f5.write(line.strip() + "\n")
            elif (1000 * 10000) < cnt <= (1200 * 10000):
                f6.write(line.strip() + "\n")
            elif (1200 * 10000) < cnt <= (1400 * 10000):
                f7.write(line.strip() + "\n")
            elif (1400 * 10000) < cnt <= (1600 * 10000):
                f8.write(line.strip() + "\n")
            elif (1600 * 10000) < cnt <= (1800 * 10000):
                f9.write(line.strip() + "\n")
            elif (1800 * 10000) < cnt <= (2000 * 10000):
                f10.write(line.strip() + "\n")
            elif (2000 * 10000) < cnt <= (2200 * 10000):
                f11.write(line.strip() + "\n")
            elif (2200 * 10000) < cnt <= (2400 * 10000):
                f12.write(line.strip() + "\n")
            elif (2400 * 10000) < cnt <= (2600 * 10000):
                f13.write(line.strip() + "\n")
            elif (2600 * 10000) < cnt <= (3000 * 10000):
                f14.write(line.strip() + "\n")

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    f7.close()
    f8.close()
    f9.close()
    f10.close()
    f11.close()
    f12.close()
    f13.close()
    f14.close()
    print("--over--")


