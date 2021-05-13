import numpy as np

L1_4 = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L1 = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
L2 = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
L3_4 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
L3 = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
L4 = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L5 = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
L6 = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
L7 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
L8 = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
L9 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
L10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

L = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])


def get_matrix_m(matrix):
    # Shape of matrix
    rows, columns = matrix.shape
    matrix_m = np.zeros([rows, columns], dtype=float)

    # Count outgoing links
    c = np.zeros([rows], dtype=int)
    for row_ind, row in enumerate(matrix):
        c[row_ind] = np.sum(row)

    # Fill stochastic matrix M
    for row_ind, row in enumerate(matrix):
        if c[row_ind] > 0:
            for col_ind, value in enumerate(row):
                matrix_m[col_ind][row_ind] = value / c[row_ind]

    # Return stochastic matrix
    return matrix_m, c


def calculate_page_rank(matrix, damping_factor, iterations):
    # Shape of matrix
    rows, columns = matrix.shape

    # Result - page rank array
    value = 1 / rows
    page_rank = np.full(rows, value, dtype=float)

    # Loop to fill array
    for _iteration in range(iterations):
        temp_page_rank = np.empty_like(page_rank)
        for r_ind in range(rows):
            # Sum in line
            cal_sum = 0.0

            for ii, val in enumerate(matrix[r_ind]):
                cal_sum += val * page_rank[ii]

            # Save result to page rank's array
            temp_page_rank[r_ind] = damping_factor + cal_sum * (1-damping_factor)

        # Normalize values calculated in iteration
        row_sum = np.sum(temp_page_rank)
        if row_sum == 0.0:
            page_rank = np.zeros_like(temp_page_rank, dtype=float)
        else:
            page_rank = np.divide(temp_page_rank, row_sum)

    # Return prepared page rank array
    return page_rank


def calculate_trust_rank(matrix, damping_factor, iterations, good_indexes_array):
    # Shape of matrix
    rows, columns = matrix.shape

    # Result - trust rank array
    bonuses = np.zeros(rows, dtype=float)
    for index in good_indexes_array:
        bonuses[index] = 1

    # Normalize
    row_sum = np.sum(bonuses)
    bonuses = np.divide(bonuses, row_sum)
    trust_rank = bonuses.copy()

    # Loop to calculate TrustRank values
    for _iteration in range(iterations):
        for r_ind in range(rows):
            # Sum in line
            cal_sum = 0.0

            for i, val in enumerate(matrix[r_ind]):
                cal_sum += val * trust_rank[i]

            # Save result to page rank's array
            trust_rank[r_ind] = bonuses[r_ind] * damping_factor + cal_sum * (1-damping_factor)

        # Normalize values calculated in iteration
        row_sum = np.sum(trust_rank)
        trust_rank = np.divide(trust_rank, row_sum)

    # Return TrustRank array
    return trust_rank


def main():
    # Debug setup
    debug = True

    # Print details of matrix L - indices
    if debug:
        print('Matrix L (indices)')
        print(L)

    # Calculate matrix M
    print('\nExercise 1')
    matrix_m, c_value = get_matrix_m(L)

    # Print details of stochastic matrix M
    if debug:
        print('Matrix M (stochastic matrix)')
        print(matrix_m)

    # TODO 2: compute PageRank with damping factor q = 0.15 [DONE]
    # Then, sort and print: (page index (first index = 1 add +1) : pagerank)
    # (use regular array + sort method + lambda function)
    print('\nExercise 2')

    if debug:
        print('Calculate PageRank vector')

    q_pr = 0.15
    pr_no_iterations = 100
    pr = calculate_page_rank(matrix_m, q_pr, pr_no_iterations)
    if debug:
        rows, columns = matrix_m.shape
        pr_indexed = np.empty(columns, dtype=object)

        for index, value in enumerate(pr):
            pr_indexed[index] = (index + 1, value)

        sorted_pr = sorted(pr_indexed, key=lambda x: x[1], reverse=True)
        for index, (page_number, page_rank) in enumerate(sorted_pr):
            print(str(page_number) + '\t' + str(index + 1) + '\t' + str(page_rank))

    # TODO 3: compute TrustRank with damping factor q = 0.15 [DONE]
    # Documents that are good = 1, 2 (indexes = 0, 1)
    # Then, sort and print: (page index (first index = 1, add +1) : trustrank)
    # (use regular array + sort method + lambda function)
    print('\nExercise 3')
    q_tr = 0.15
    tr_no_iterations = 100
    good_indexes = [0, 1]
    tr = calculate_trust_rank(matrix_m, q_tr, tr_no_iterations, good_indexes)
    if debug:
        print("TrustRank (DOCUMENTS 1 AND 2 ARE GOOD)")
        rows, columns = matrix_m.shape
        tr_indexed = np.empty(columns, dtype=object)

        for index, value in enumerate(tr):
            tr_indexed[index] = (index + 1, value)

        sorted_tr = sorted(tr_indexed, key=lambda x: x[1], reverse=True)
        for index, (page_number, trust_rank) in enumerate(sorted_tr):
            print(str(page_number) + '\t' + str(index + 1) + '\t' + str(trust_rank))

    # TODO 4: Repeat TODO 3 but remove the connections 3->7 and 1->5 (indexes: 2->6, 0->4)
    print('\nExercise 4')
    l_matrix = np.array([L1_4, L2, L3_4, L4, L5, L6, L7, L8, L9, L10])
    matrix_m, cc = get_matrix_m(l_matrix)
    q_tr = 0.15
    tr_no_iterations = 1
    good_indexes = [0, 1]
    tr = calculate_trust_rank(matrix_m, q_tr, tr_no_iterations, good_indexes)
    if debug:
        print("TrustRank (DOCUMENTS 1 AND 2 ARE GOOD)")
        rows, columns = matrix_m.shape
        tr_indexed = np.empty(columns, dtype=object)

        for index, value in enumerate(tr):
            tr_indexed[index] = (index + 1, value)

        sorted_tr = sorted(tr_indexed, key=lambda x: x[1], reverse=True)
        for index, (page_number, trust_rank) in enumerate(sorted_tr):
            print(str(page_number) + '\t' + str(index + 1) + '\t' + str(trust_rank))


if __name__ == "__main__":
    main()
