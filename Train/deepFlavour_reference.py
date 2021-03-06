

from training_base import training_base
from Losses import loss_NLL
from modelTools import fixLayersContaining

#also does all the parsing
train=training_base(testrun=True)

newtraining= not train.modelSet()
#for recovering a training
if True or newtraining:
    from models import model_deepFlavourReference
    
    train.setModel(model_deepFlavourReference,dropoutRate=0.1)
    
    #train.keras_model=fixLayersContaining(train.keras_model, 'regression', invert=False)
    
    train.compileModel(learningrate=0.001,
                       loss=['categorical_crossentropy',loss_NLL],
                       metrics=['accuracy'],
                       loss_weights=[1., 0.00000001])


print(train.keras_model.summary())
model,history = train.trainModel(nepochs=1, 
                                 batchsize=10000, 
                                 stop_patience=300, 
                                 lr_factor=0.5, 
                                 lr_patience=3, 
                                 lr_epsilon=0.0001, 
                                 lr_cooldown=6, 
                                 lr_minimum=0.0001, 
                                 maxqsize=100)


print('indentification training finished. Starting regression training...')

train.saveCheckPoint('IDonly')

train.keras_model=fixLayersContaining(train.keras_model, 'regression', invert=True)
train.compileModel(learningrate=0.001,
                       loss=['categorical_crossentropy',loss_NLL],
                       metrics=['accuracy'],
                       loss_weights=[1., 1])

train.trainedepoches=0
print(train.keras_model.summary())



model,history = train.trainModel(nepochs=1, 
                                 batchsize=10000, 
                                 stop_patience=300, 
                                 lr_factor=0.5, 
                                 lr_patience=3, 
                                 lr_epsilon=0.0001, 
                                 lr_cooldown=6, 
                                 lr_minimum=0.0001, 
                                 maxqsize=100)
