import bnlearn as bn
from pgmpy.factors.discrete import TabularCPD
import matplotlib.pyplot as plt

# Define Edges:
edges = [('1', '2'),
         ('1', '5'),
         ('2', '4'),
         ('0', '4'),
         ('3', '4')]

#Make DAG from edges defined above
DAG = bn.make_DAG(edges)
bn.plot(DAG)

node_0 = TabularCPD(variable='0', variable_card=2, values=[[0.64], [0.36]])
#print(node_0)

node_1 = TabularCPD(variable='1', variable_card=2, values=[[0.6], [0.4]])
#print(node_1)

node_2 = TabularCPD(variable='2', variable_card=2, 
                    values=[[0.17, 0.3],
                            [0.83, 0.7]],
                    evidence = ['1'],
                    evidence_card=[2])
#print(node_2)

node_3 = TabularCPD(variable='3', variable_card=2, values=[[0.6], [0.4]])
#print(node_3)


node_4 = TabularCPD(variable='4', variable_card=2, 
                    values=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 
                            [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]],
                    evidence = ['3', '2', '0'],
                    evidence_card=[2, 2, 2])
#print(node_4)

node_5 = TabularCPD(variable='5', variable_card=2, 
                    values=[[0.17, 0.3],
                            [0.83, 0.7]],
                    evidence = ['1'],
                    evidence_card=[2])
#print(node_5)

model = bn.make_DAG(DAG, CPD = [node_0, node_1, node_2, node_3, node_4, node_5])
#bn.print_CPD(DAG)
bn.plot(model)
#plt.savefig("b_net.png")

# Step 4: Generate Data from the Bayesian Network
sample_sizes = [100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
#sample_sizes = [100, 1000]
results = []

for sample_size in sample_sizes:

        df = bn.sampling(model, n=sample_size)

        # Step 5: Learn the Structure
        model_learned = bn.structure_learning.fit(df)

        # Step 6: Learn CPTs with the new structure
        model_learned_w_params = bn.parameter_learning.fit(model_learned, df)

        # Step 7: Learn CPTs using the original structure
        model_original_w_params = bn.parameter_learning.fit(model, df)

        # Step 8: Store results
        results.append({'n': sample_size, 'learned_structure': model_learned, 'learned_CPTs': model_learned_w_params})


        # Step 9: Plot learned structure        
        bn.plot(model_learned)
        cpt_dict = bn.print_CPD(model_learned, verbose=False)

        with open("figures/model_learned_n" + str(sample_size), "w") as f:
                for node, cpt in cpt_dict.items():
                        f.write(f"Node: {node}\n")
                        f.write(str(cpt) + "\n\n") 

        path = "figures/model_learned_n" + str(sample_size)
        plt.savefig(path, bbox_inches="tight")       
        
        
        bn.plot(model_learned_w_params)
        cpt_dict = bn.print_CPD(model_learned_w_params, verbose=False)

        with open("figures/model_learned_w_params_n" + str(sample_size), "w") as f:
                for node, cpt in cpt_dict.items():
                        f.write(f"Node: {node}\n")
                        f.write(str(cpt) + "\n\n") 

        path = "figures/model_learned_w_params_n" + str(sample_size)
        plt.savefig(path, bbox_inches="tight")       
        
        bn.plot(model_original_w_params)
        cpt_dict = bn.print_CPD(model_original_w_params, verbose=False)
        with open("figures/model_original_w_param_n" + str(sample_size), "w") as f:
                for node, cpt in cpt_dict.items():
                        f.write(f"Node: {node}\n")
                        f.write(str(cpt) + "\n\n") 
        
        path = "figures/model_original_w_params_n" + str(sample_size)
        plt.savefig(path, bbox_inches="tight")



print("Finished!")