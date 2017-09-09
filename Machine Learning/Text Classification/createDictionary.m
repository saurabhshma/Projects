function [dict, X] = createDictionary(X, dataSize) 
  for(i = 1:dataSize)
    X{i} = (strsplit(X{i}));
  end
  dict=unique([X{:}]);
end