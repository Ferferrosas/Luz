function [LDA, SVM, KNN, DT, NB] = xvalidation_FtRan(dataFt,dataLabel, A, movement, trial, idx, m, n)
%[LDA, SVM, KNN, DT, NB]
% Apply Croos-Validation and Different Classifiers to predict data (LDA, SVM, KNN, DT, NB),
% returns the variable Fran with the average after apply the classifiers.
accuracy1 = zeros(A,1);
accuracy2 = zeros(A,1);
accuracy3 = zeros(A,1);
accuracy4 = zeros(A,1);
accuracy5 = zeros(A,1);
Y = (movement * trial)/5;

dataFt = cat(2,dataFt, dataLabel);
%     Sort_dataFt = dataFt(randperm(size(dataFt,1)),:);
%     Sort_Ft = Sort_dataFt(:,1:end-1);
%     Sort_dataLabel = Sort_dataFt(:,112);

for r = 1:A
    
    Sort_dataFt = dataFt(randperm(size(dataFt,1)),:);
    Sort_Ft = Sort_dataFt(:,1:end-1);
    [~,B] = size(Sort_dataFt);
    Sort_dataLabel = Sort_dataFt(:,B);
    
    [A,~] = size(Sort_Ft);
    trainFeatures = Sort_Ft(1:A*.8,:);
    trainLabels = Sort_dataLabel(1:A*.8);
    
    testFeatures = Sort_Ft(A*.8+1:end,:);
    testLabels = Sort_dataLabel(A*.8+1:end);
    %         testFeatures = Sort_Ft((r - 1) * Y + 1 : r * Y,:);
    %         testLabels = Sort_dataLabel((r - 1) * Y + 1 : r * Y);
    %         if r==1
    %             trainFeatures = Sort_Ft(Y + 1 : end, :);
    %             trainLabels = Sort_dataLabel(Y + 1 : end);
    %         elseif r<A
    %             trainFeatures = [Sort_Ft(1:(r-1)*Y:(r-1)*Y,:);Sort_Ft(r*Y+1:end,:)];
    %             trainLabels = [Sort_dataLabel(1:(r-1)*Y:(r-1)*Y);Sort_dataLabel(r*Y+1:end)];
    %         else
    %             trainFeatures = Sort_Ft(1:(r-1)*Y,:);
    %             trainLabels = Sort_dataLabel(1:(r-1)*Y);
    %         end
    LDA_Mdl = fitcdiscr(trainFeatures(:,idx(:,1:m(:,n))),trainLabels);
    [label1,~] = predict(LDA_Mdl,testFeatures(:,idx(:,1:m(:,n))));
    accuracy1(r) = sum(label1 == testLabels)/length(testLabels);
    
    SVM_Mdl = fitcecoc(trainFeatures(:,idx(:,1:m(:,n))),trainLabels);
    [label2,~] = predict(SVM_Mdl,testFeatures(:,idx(:,1:m(:,n))));
    accuracy2(r) = sum(label2 == testLabels)/length(testLabels);
    
    KNN_Mdl = fitcknn(trainFeatures(:,idx(:,1:m(:,n))),trainLabels);
    [label3,~] = predict(KNN_Mdl,testFeatures(:,idx(:,1:m(:,n))));
    accuracy3(r) = sum(label3 == testLabels)/length(testLabels);
    
    DT_Mdl = fitctree(trainFeatures(:,idx(:,1:m(:,n))),trainLabels);
    [label4,~] = predict(DT_Mdl,testFeatures(:,idx(:,1:m(:,n))));
    accuracy4(r) = sum(label4 == testLabels)/length(testLabels);
    
    NB_Mdl = fitcnb(trainFeatures(:,idx(:,1:m(:,n))),trainLabels);
    [label5,~] = predict(NB_Mdl,testFeatures(:,idx(:,1:m(:,n))));
    accuracy5(r) = sum(label5 == testLabels)/length(testLabels);
end
LDA = mean(accuracy1);
SVM = mean(accuracy2);
KNN = mean(accuracy3);
DT = mean(accuracy4);
NB = mean(accuracy5);
end