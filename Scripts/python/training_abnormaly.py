from IPython.display import clear_output

adagrad=Adagrad(lr=0.01, epsilon=1e-08)

model.compile(loss=custom_objective, optimizer=adagrad)

print("Starting training...")

AllClassPath='/content/gdrive/My Drive/Code/Train'
# AllClassPath contains C3D features (.txt file)  of each video. Each text file contains 32 features, each of 4096 dimension
output_dir='/content/gdrive/My Drive/Code/Trained_13Actions/'
loss_dir = '/content/gdrive/My Drive/Code/Trained_13Actions/Loss'
# Output_dir is the directory where you want to save trained weights
weights_path = output_dir + 'weights.mat'
# weights.mat are the model weights that you will get after (or during) that training
model_path = output_dir + 'model.json'

if not os.path.exists(output_dir):
       os.makedirs(output_dir)
    
if not os.path.exists(loss_dir):
       os.makedirs(loss_dir)
    
All_class_files= listdir(AllClassPath)
All_class_files.sort()
loss_graph =[]
num_iters = 20000
total_iterations = 0
batchsize=60
time_before = datetime.now()

for it_num in range(num_iters):

    AbnormalPath = os.path.join(AllClassPath, All_class_files[0])  # Path of abnormal already computed C3D features
    NormalPath = os.path.join(AllClassPath, All_class_files[1])    # Path of Normal already computed C3D features
    inputs, targets=load_dataset_Train_batch(AbnormalPath, NormalPath)  # Load normal and abnormal video C3D features
    # targets of length 1920 (32*60 video)
    # INPUT: 
    #   1/ A BATCH of 1920 feature vector (4096d) for each segment, 810 abnormal, 798 normal
    #   2/ LABEL of 1920 segments, integer value 0/1 (regression)
    batch_loss =model.train_on_batch(inputs, targets)
    loss_graph = np.hstack((loss_graph, batch_loss)) #put to stack of numpy array
    total_iterations += 1
    # PLOT THE LOSS
    plt.plot(loss_graph, label='loss')
    plt.title('MIL Ranking Loss')
    plt.legend()
    plt.xlabel('Number of iteration')
    plt.ylabel('Loss')
    if total_iterations % 20 == 1:
      plt.savefig(loss_dir + 'loss_' + str(total_iterations) +'.png')
      print "These iteration=" + str(total_iterations) + ") took: " + str(datetime.now() - time_before) + ", with loss of " + str(batch_loss)
    plt.show()
    if total_iterations % 20 == 1:
        iteration_path = output_dir + 'Iterations_graph_' + str(total_iterations) + '.mat'
        savemat(iteration_path, dict(loss_graph=loss_graph))
        clear_output()
    if total_iterations % 1000 == 0:  # Save the model at every 1000th iterations.
       weights_path = output_dir + 'weights_L1L2' + str(total_iterations) + '.mat'
       save_model(model, model_path, weights_path)


save_model(model, model_path, weights_path)
