if [ -d "dist" ]; then
echo "Removing distribution directory."
rm -r dist
fi
pyinstaller queriet.spec
cp -r plugins dist