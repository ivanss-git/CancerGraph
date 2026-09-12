import numpy as np
import sys

def main():
    # Known association matrix Y (miRNAs x diseases)
    Y = np.array([
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])

    # 1. Calculate miRNA Similarity Matrix (S_m) using rows of Y
    N = Y.shape[0]
    S_m = np.eye(N)

    for i in range(N):
        for j in range(i+1, N):
            dot_product = np.dot(Y[i], Y[j])
            norm_i = np.linalg.norm(Y[i])
            norm_j = np.linalg.norm(Y[j])
            sim = dot_product / (norm_i * norm_j) if (norm_i * norm_j) > 0 else 0.0
            S_m[i, j] = sim
            S_m[j, i] = sim

    # 2. Calculate Disease Similarity Matrix (S_d) using columns of Y
    M = Y.shape[1]
    S_d = np.eye(M)

    for i in range(M):
        for j in range(i+1, M):
            dot_product = np.dot(Y[:, i], Y[:, j])
            norm_i = np.linalg.norm(Y[:, i])
            norm_j = np.linalg.norm(Y[:, j])
            sim = dot_product / (norm_i * norm_j) if (norm_i * norm_j) > 0 else 0.0
            S_d[i, j] = sim
            S_d[j, i] = sim

    # 3. CONSTRUCT THE LATENT SPACES (k=2 dimensions)
    rng = np.random.default_rng(42)
    X = rng.random((3, 2))
    W = rng.random((3, 2))

    # Run regularized factorization
    learning_rate = 0.01
    alpha, beta = 0.5, 0.5

    for epoch in range(1000):
        error = Y - np.dot(X, W.T)
        
        # Standard decomposition gradients
        grad_X = -2 * np.dot(error, W)
        grad_W = -2 * np.dot(error.T, X)
        
        # Calculate Graph Laplacians (L = D - S)
        L_m = np.diag(np.sum(S_m, axis=1)) - S_m
        L_d = np.diag(np.sum(S_d, axis=1)) - S_d
        
        # Add graph penalty gradients to preserve similarity structures
        grad_X += 2 * alpha * np.dot(L_m, X)
        grad_W += 2 * beta * np.dot(L_d, W)
        
        # Apply updates
        X -= learning_rate * grad_X
        W -= learning_rate * grad_W

    Y_predicted = np.dot(X, W.T)

    print("--- Final Model Output ---")
    print(np.round(Y_predicted, 3))

if __name__ == "__main__":
    sys.exit(main())
