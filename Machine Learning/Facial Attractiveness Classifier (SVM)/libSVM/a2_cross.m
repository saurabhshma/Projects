tic;
data = load('traindata.txt');
labels = load('trainlabels.txt');

labels(labels==2)= -1;


x = load('testdata.txt');
y = load('testlabels.txt');
y(y==2) = -1;

options = {'-s 0 -t 2 -g 2.5 -v 10'};
c = [{' -c 1'},{' -c 10'},{' -c 100'},{' -c 1000'},{' -c 10000'},{' -c 100000'},{' -c 1000000'}];
options_test = {'-s 0 -t 2 -g 2.5'};

accuracy = ones(length(c),1);
acc_cross = ones(length(c),1)
for i = 1:length(c)
  opt = strcat(options,c{1,i}); 
  opt = char(opt);
  acc_cross(i) = svmtrain(labels,data,opt);
  
  opt2 = strcat(options_test,c{1,i});
  opt2 = char(opt2);
  gauss_model = svmtrain(labels,data,opt2);

  gauss_res = svmpredict(y,x,gauss_model);
  diff = gauss_res == y;
  accuracy(i) = (sum(diff)/length(diff))*100;
  
end

c_plot = [1,10,100,1000,10000,100000,1000000];

figure();
hold on;
plot(log10(c_plot),accuracy,'+');
plot(log10(c_plot),acc_cross,'*');
xlabel('log c');
ylabel('Accuracy');
title('Graph of Accuracy vs log c');
legend('test set accuracy','cross-validation accuracy');
hold off;



%gauss_res = svmpredict(y,x,gauss_model);

%my_model.sv_indices
%gauss_model
toc;