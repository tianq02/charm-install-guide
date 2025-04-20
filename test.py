from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT
def main():
    # 初始化配对群
    group = PairingGroup('MNT224')

    # 生成两个随机元素
    a = group.random(ZR)
    b = group.random(ZR)

    # 计算两个元素的乘积
    result = a * b

    print(f"随机元素 a: {a}")
    print(f"随机元素 b: {b}")
    print(f"a 和 b 的乘积: {result}")

if __name__ == "__main__":
    main()

