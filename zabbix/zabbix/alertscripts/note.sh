yum install -y  python3-pip 
if [ $? -eq 0 ]; then
  pip3 install requests
fi
if [ $? -eq 0 ] ; then

   echo "need soft is done"
fi
