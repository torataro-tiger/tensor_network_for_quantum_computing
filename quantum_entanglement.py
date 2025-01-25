import argparse
from typing import Literal

import numpy as np
import tensornetwork as tn

QuantumState = Literal["00", "01", "10", "11"]


def calc_prob(quantum_state: QuantumState) -> None:
    O = np.array([[0, 0], [0, 0]])
    I = np.array([[1, 0], [0, 1]])
    X = np.array([[0, 1], [1, 0]])
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # アダマールゲート定義
    CX = np.array([[I, O], [O, X]])  # CXゲート定義
    zero_state = np.array([1, 0])  # |0>状態定義
    one_state = np.array([0, 1])  # |1>状態定義

    H_node = tn.Node(H, name="Hadamard Gate")  # アダマールゲートノード化
    CX_node = tn.Node(CX, name="Controlled NOT Gate")  # CXゲートノード化
    init_node_1 = tn.Node(zero_state, name="zero_init_state")  # 初期状態|q_1>=|0>ノード化
    init_node_0 = tn.Node(zero_state, name="zero_init_state")  # 初期状態|q_0>=|0>ノード化
    zero_final_node_1 = tn.Node(zero_state, name="zero_final_state")  # 終状態|q'_1>=|0>ノード化
    zero_final_node_0 = tn.Node(zero_state, name="zero_final_state")  # 終状態|q'_0>=|0>ノード化
    one_final_node_1 = tn.Node(one_state, name="one_final_state")  # 終状態|q'_1>=|1>ノード化
    one_final_node_0 = tn.Node(one_state, name="one_final_state")  # 終状態|q'_0>=|1>ノード化

    if quantum_state == "00":
        final_node_1 = zero_final_node_1  # 終状態の設定|q'_1>
        final_node_0 = zero_final_node_0  # 終状態の設定|q'_0>
    if quantum_state == "01":
        final_node_1 = one_final_node_1  # 終状態の設定|q'_1>
        final_node_0 = zero_final_node_0  # 終状態の設定|q'_0>
    if quantum_state == "10":
        final_node_1 = zero_final_node_1  # 終状態の設定|q'_1>
        final_node_0 = one_final_node_0  # 終状態の設定|q'_0>
    if quantum_state == "11":
        final_node_1 = one_final_node_1  # 終状態の設定|q'_1>
        final_node_0 = one_final_node_0  # 終状態の設定|q'_0>

    # |q_1>から|q'_1>までの脚の結合
    tn.connect(H_node[1], init_node_1[0])  # 初期状態|q_1>とアダマールゲートの結合
    tn.connect(CX_node[1], H_node[0])  # アダマールゲートとCXゲートの結合
    tn.connect(final_node_1[0], CX_node[0])  # CXゲートと終状態|q'_1>の結合
    # |q_0>から|q'_0>までの脚の結合
    tn.connect(CX_node[3], init_node_0[0])  # 初期状態|q_0>とCXゲートの結合
    tn.connect(final_node_0[0], CX_node[2])  # CXゲートと終状態|q'_0>の結合

    # 縮約
    result = tn.contractors.auto([init_node_1, init_node_0, H_node, CX_node, final_node_1, final_node_0])

    # 確率計算
    prob = np.abs(result.tensor) ** 2
    print(f"量子状態|{quantum_state}>の観測確率は{prob}です。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="量子もつれ状態の観測確率を計算するコードです。")
    parser.add_argument(
        "--quantum_state",
        type=str,
        choices=["00", "01", "10", "11"],
        default="00",
        help="初期量子状態|q_0q_1>です。00, 01, 10, 11から選択してください。",
    )
    args = parser.parse_args()
    quantum_state = args.quantum_state

    calc_prob(quantum_state)
