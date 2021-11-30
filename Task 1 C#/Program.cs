using System;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;

namespace HardDiskInfo
{
    class Program
    {
        class Person
        {
            public string Name { get; set; }
        }

        public static void file()
        {
            Console.WriteLine("\nEnter file name: ");
            string path = Console.ReadLine();

            Console.WriteLine("Enter file data:");
            string text = Console.ReadLine();

            using (FileStream fstream = new FileStream(path, FileMode.OpenOrCreate))
            {
                byte[] array = System.Text.Encoding.Default.GetBytes(text);
                fstream.Write(array, 0, array.Length);
            }

            using (FileStream fstream = File.OpenRead(path))
            {
                byte[] array = new byte[fstream.Length];
                fstream.Read(array, 0, array.Length);
                string textFromFile = System.Text.Encoding.Default.GetString(array);
                Console.WriteLine($"File data: {textFromFile}");
            }

            FileInfo fileInf = new FileInfo(path);
            if (fileInf.Exists)
            {
                fileInf.Delete();
                // альтернатива с помощью класса File
                // File.Delete(path);
            }
        }

        public static async Task jsonfile()
        {
            Console.WriteLine("\nEnter JSON file name: ");
            string path = Console.ReadLine();

            Console.WriteLine("Enter string:");
            string text = Console.ReadLine();

            using (FileStream fs = new FileStream(path + ".json", FileMode.OpenOrCreate))
            {
                Person tom = new Person() { Name = text };
                await JsonSerializer.SerializeAsync<Person>(fs, tom);
            }
            using (FileStream fs = new FileStream(path + ".json", FileMode.OpenOrCreate))
            {
                Person restoredPerson = await JsonSerializer.DeserializeAsync<Person>(fs);
                Console.WriteLine($"JSON data : {restoredPerson.Name}");
            }
            File.Delete(path + ".json");
        }

        public static void xmlfile()
        {
            XDocument xdoc = new XDocument();
            Console.WriteLine("\nEnter XML file name: ");
            string path = Console.ReadLine();
            XElement file = new XElement(path + ".xml");
            XAttribute NameAttr = new XAttribute("name", "Snoopy");
            XElement ageElem = new XElement("age", "5");
            file.Add(NameAttr);
            file.Add(ageElem);

            xdoc.Add(file);
            xdoc.Save(path + ".xml");

            var doc = new XmlDocument();
            doc.Load(path + ".xml");
            var root = doc.DocumentElement;
            PrintItem(root);
            File.Delete(path + ".xml");
        }

        /// <param name="item"> XML Element. </param>
        /// <param name="indent"> Indent count from string beginning. </param>
        private static void PrintItem(XmlElement item, int indent = 0)
        {
            Console.Write($"{new string('\t', indent)}{item.LocalName} ");
            foreach (XmlAttribute attr in item.Attributes)
            {
                Console.Write($"[{attr.InnerText}]");
            }
            foreach (var child in item.ChildNodes)
            {
                if (child is XmlElement node)
                {

                    Console.WriteLine();
                    PrintItem(node, indent + 1);
                }

                if (child is XmlText text)
                {
                    Console.Write($"- {text.InnerText}");
                }
            }
        }

        public static void zip()
        {
            const string archivePath = @"C:\archive.zip";
            using (ZipArchive zipArchive = ZipFile.Open(archivePath, ZipArchiveMode.Create))
            {
                const string pathFileToAdd = @"C:\test.txt";
                const string nameFileToAdd = "test.txt";
                zipArchive.CreateEntryFromFile(pathFileToAdd, nameFileToAdd);
            }
            using (ZipArchive zipArchive = ZipFile.OpenRead(archivePath))
            {
                const string nameExtractFile = "test.txt";
                const string pathExtractFile = @"C:\unarchivedTest.txt";
                zipArchive.Entries.FirstOrDefault(x => x.Name == nameExtractFile)?.
                    ExtractToFile(pathExtractFile);
            }
        }

        static void Main(string[] args)
        {
            DriveInfo[] drives = DriveInfo.GetDrives();
            foreach (DriveInfo drive in drives)
            {
                Console.WriteLine($"Name: {drive.Name}");
                Console.WriteLine($"Type: {drive.DriveType}");
                Console.WriteLine($"File System: {drive.DriveFormat}");
                //Console.WriteLine($"Type: {drive}");
                if (drive.IsReady)
                {
                    Console.WriteLine($"Size: {drive.TotalSize}");
                    Console.WriteLine($"Free space: {drive.TotalFreeSpace}");
                    Console.WriteLine($"Label: {drive.VolumeLabel}");
                }
                Console.WriteLine("========================\n");
            }

            file(); // Запись в файл информации и последующее чтение
            jsonfile(); // Создание, запись и чтение информации и удаление json файла
            xmlfile(); // Создание и запись в xml файл
            zip();
        }


    }
}
