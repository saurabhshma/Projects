Xtrain=load('traindata.txt');          %load training data
Ytrain=load('trainlabels.txt');  %load labels of training data
Xtest=load('testdata.txt');      %load test data
Ytest=load('testlabels.txt');    %load labels of test data


model_lin = svmtrain(Ytrain, Xtrain, '-c 500 -t 0');  %linear model
[predict_label, accuracy_lin, dec_values] = svmpredict(Ytest, Xtest, model_lin);  %accuracy on test for linear model
model_gaus = svmtrain(Ytrain, Xtrain, '-c 500 -g 2.5');                           %gaussian model
[predict_label, accuracy_gaus, dec_values] = svmpredict(Ytest, Xtest, model_gaus);  %accuracy on test for gaussian model
accuracy_lin(1)                               %linear accuracy for C=500
accuracy_gaus(1)                              %gaussian accuracy for C=500
model_lin.sv_indices                          %sv index for linear
model_gaus.sv_indices                         %sv index for gaussian
x=1;
test_acc=zeros(7,1);
cross_acc=zeros(7,1);
log_c=zeros(7,1);
max_c=1;
max_acc=0;
%calculating cross validation and test accuracy for different values of C
for i=1:7
  log_c(i)=log10(x);
  acc_cros=svmtrain(Ytrain, Xtrain, sprintf("-s 0 -t 2 -c %d -g 2.5 -v 10",x));
  model_gaus_cros = svmtrain(Ytrain, Xtrain, sprintf("-t 2 -c %d -g 2.5",x));
  [predict_label, accuracy_gaus_cros, dec_values] = svmpredict(Ytest, Xtest, model_gaus_cros);
  test_acc(i)=accuracy_gaus_cros(1);
  cross_acc(i)=acc_cros;
  if(max_acc<acc_cros)
      max_c=x;
      max_acc=acc_cros;
  end
  x=x*10;
end
%plot figure
figure();
max_c
hold on;
plot(log_c, test_acc, 'r.', 'MarkerSize', 8);  
plot(log_c, cross_acc, 'b.', 'MarkerSize', 8);
legend('test set accuracy', 'cross validation accuracy');

xlabel('log C');
ylabel('Accuracy');
hold off;


